"""
Rate Limiting Middleware for FairPayCheck API
Simple in-memory IP-based rate limiting (30 requests per minute)
"""

import time
import requests
from collections import defaultdict
from django.http import JsonResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from user_agents import parse


class RateLimitMiddleware:
    """
    Simple rate limiting middleware.
    Limits API endpoints to 30 requests per minute per IP.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = defaultdict(list)
        self.rate_limit = 30  # requests
        self.time_window = 60  # seconds
    
    def __call__(self, request):
        # Only rate limit API endpoints
        if request.path.startswith('/api/'):
            client_ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests outside the time window
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < self.time_window
            ]
            
            # Check if rate limit exceeded
            if len(self.requests[client_ip]) >= self.rate_limit:
                return JsonResponse({
                    'error': 'Rate limit exceeded. Please try again later.',
                    'retry_after': self.time_window
                }, status=429)
            
            # Record this request
            self.requests[client_ip].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Extract client IP from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip


class VisitorTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track visitors and page views
    Captures IP, geolocation, device info, and logs all page views
    """
    
    # Bot user agents to exclude
    BOT_USER_AGENTS = [
        'bot', 'crawler', 'spider', 'scraper', 'headless',
        'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider'
    ]
    
    def process_request(self, request):
        """Process incoming request to track visitor"""
        # Import here to avoid circular imports
        from core.models import VisitorLog, PageView
        
        # Skip tracking for admin, static files, and media
        if request.path.startswith(('/admin/', '/static/', '/media/')):
            return None
        
        # Get IP address
        ip_address = self.get_client_ip(request)
        if not ip_address:
            return None
        
        # Get or create session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        # Parse user agent
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)
        
        # Get device type and browser first
        device_type = self.get_device_type(user_agent)
        browser = user_agent.browser.family
        
        # Check if bot - also check browser name and device type
        is_bot = self.is_bot(user_agent_string, browser, device_type)
        
        # Get or create visitor log
        visitor_log, created = VisitorLog.objects.get_or_create(
            ip_address=ip_address,
            defaults={
                'session_key': session_key,
                'user_agent': user_agent_string,
                'browser': browser,
                'browser_version': user_agent.browser.version_string,
                'device_type': device_type,
                'os': user_agent.os.family,
                'os_version': user_agent.os.version_string,
                'is_bot': is_bot,
                'is_mobile': user_agent.is_mobile,
                'referrer': request.META.get('HTTP_REFERER'),
                'landing_page': request.path,
            }
        )
        
        # Fetch geolocation data if not already set
        if created and not visitor_log.country:
            self.update_geolocation(visitor_log, ip_address)
        
        # Update visitor log if not created
        if not created:
            visitor_log.increment_visit()
            visitor_log.last_visit = timezone.now()
            visitor_log.save(update_fields=['last_visit', 'total_visits'])
        
        # Create page view record
        PageView.objects.create(
            visitor=visitor_log,
            url=request.path,
            page_title=self.get_page_title(request),
            method=request.method,
            ip_address=ip_address,
            user_agent=user_agent_string,
            referrer=request.META.get('HTTP_REFERER'),
            session_key=session_key,
            country_code=visitor_log.country_code,
            device_type=visitor_log.device_type,
        )
        
        # Increment total page views
        visitor_log.total_page_views += 1
        visitor_log.save(update_fields=['total_page_views'])
        
        # Attach visitor to request for later use
        request.visitor = visitor_log
        
        return None
    
    def get_client_ip(self, request):
        """
        Get client's real IP address
        Handles proxies and load balancers
        """
        # Try various headers used by proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # X-Forwarded-For can contain multiple IPs, take the first one
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Try other common headers
            ip = (
                request.META.get('HTTP_X_REAL_IP') or
                request.META.get('HTTP_CF_CONNECTING_IP') or  # Cloudflare
                request.META.get('REMOTE_ADDR')
            )
        return ip
    
    def get_device_type(self, user_agent):
        """Determine device type from user agent"""
        if user_agent.is_mobile:
            return 'Mobile'
        elif user_agent.is_tablet:
            return 'Tablet'
        elif user_agent.is_pc:
            return 'Desktop'
        else:
            return 'Unknown'
    
    def is_bot(self, user_agent_string, browser='', device_type=''):
        """
        Check if user agent is a bot
        Detects bots by:
        1. User agent string containing known bot keywords
        2. Browser name containing 'bot' or 'spider'
        3. Device type being 'Unknown'
        """
        user_agent_lower = user_agent_string.lower()
        browser_lower = browser.lower() if browser else ''
        
        # Check user agent for known bot patterns
        if any(bot in user_agent_lower for bot in self.BOT_USER_AGENTS):
            return True
        
        # Check if browser name contains 'bot' or 'spider'
        if 'bot' in browser_lower or 'spider' in browser_lower:
            return True
        
        # Mark as bot if device type is Unknown
        if device_type == 'Unknown':
            return True
        
        return False
    
    def get_page_title(self, request):
        """Extract page title from path"""
        path = request.path.strip('/')
        if not path:
            return 'Homepage'
        elif path.startswith('api/'):
            return 'API'
        else:
            return path.replace('/', ' - ').title()
    
    def update_geolocation(self, visitor_log, ip_address):
        """
        Get geolocation data from IP address using ip-api.com (free)
        Rate limit: 45 requests per minute
        """
        try:
            # Skip localhost/private IPs
            if ip_address in ['127.0.0.1', '::1'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
                return
            
            # Call free geolocation API
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}',
                timeout=2
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    visitor_log.country = data.get('country')
                    visitor_log.country_code = data.get('countryCode')
                    visitor_log.city = data.get('city')
                    visitor_log.region = data.get('regionName')
                    visitor_log.latitude = data.get('lat')
                    visitor_log.longitude = data.get('lon')
                    visitor_log.save()
        except Exception as e:
            # Silently fail - don't break the request
            print(f"Geolocation error for {ip_address}: {e}")

