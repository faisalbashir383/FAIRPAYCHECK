from django.db import models
from django.utils import timezone


class VisitorLog(models.Model):
    """
    Model to store unique visitor information based on IP address.
    Captures browser, device, geolocation, and visit statistics.
    """
    
    # Primary identifiers
    ip_address = models.CharField(max_length=45, unique=True, db_index=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    # User agent info
    user_agent = models.TextField(blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    browser_version = models.CharField(max_length=50, blank=True, null=True)
    
    # Device info
    device_type = models.CharField(max_length=20, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    os_version = models.CharField(max_length=50, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    is_mobile = models.BooleanField(default=False)
    
    # Geolocation data
    country = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Traffic source
    referrer = models.URLField(max_length=2000, blank=True, null=True)
    landing_page = models.CharField(max_length=500, blank=True, null=True)
    
    # Visit timestamps
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    
    # Statistics
    total_visits = models.PositiveIntegerField(default=1)
    total_page_views = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Visitor Log'
        verbose_name_plural = 'Visitor Logs'
        ordering = ['-last_visit']
    
    def __str__(self):
        return f"{self.ip_address} - {self.country or 'Unknown'} ({self.device_type or 'Unknown'})"
    
    def increment_visit(self):
        """Increment total visit count"""
        self.total_visits += 1


class PageView(models.Model):
    """
    Model to store individual page view records.
    Linked to VisitorLog for detailed analytics.
    """
    
    # Link to visitor
    visitor = models.ForeignKey(
        VisitorLog,
        on_delete=models.CASCADE,
        related_name='page_views'
    )
    
    # Page info
    url = models.CharField(max_length=500)
    page_title = models.CharField(max_length=200, blank=True, null=True)
    method = models.CharField(max_length=10, default='GET')
    
    # Request details
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(max_length=2000, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    # Quick access fields (denormalized for performance)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['url']),
        ]
    
    def __str__(self):
        return f"{self.url} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Author(models.Model):
    """
    Author model for E-E-A-T compliance and Google Discover eligibility.
    Each author has a public profile page with identity verification links.
    """
    
    # Identity
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    # Bio and expertise
    bio = models.TextField(help_text="Human-written bio describing real experience")
    expertise = models.TextField(
        help_text="Comma-separated expertise areas (e.g., 'Software Engineering, Data Analysis')"
    )
    
    # External identity proof (E-E-A-T)
    linkedin_url = models.URLField(help_text="LinkedIn profile URL (mandatory for E-E-A-T)")
    github_url = models.URLField(blank=True, help_text="GitHub profile URL (recommended)")
    
    # Profile image (external URL)
    profile_image = models.URLField(
        blank=True,
        help_text="Profile image URL (use GitHub raw URL, recommended 400x400)"
    )
    
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/author/{self.slug}/"
    
    def get_expertise_list(self):
        """Return expertise as a list."""
        return [e.strip() for e in self.expertise.split(',') if e.strip()]


class BlogPost(models.Model):
    """
    Blog post model for Google Discover-eligible content.
    Uses external URLs for images (GitHub raw URLs).
    """
    
    # Content fields
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=200)
    excerpt = models.TextField(help_text="Short summary for Discover & listings")
    content = models.TextField(help_text="HTML content only, no Markdown")
    
    # Featured image (external URL - e.g., GitHub raw)
    featured_image = models.URLField(
        max_length=500,
        help_text="Full URL to featured image (1200x630, use GitHub raw URL)"
    )
    
    # Author (ForeignKey for E-E-A-T)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        null=True,
        blank=True
    )
    
    # Timestamps
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=300)
    meta_description = models.CharField(max_length=160)
    
    # Publishing
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/blog/{self.slug}/"


