from django.contrib import admin
from .models import VisitorLog, PageView


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    """Admin configuration for VisitorLog model"""
    
    list_display = [
        'ip_address', 'country', 'city', 'device_type', 
        'browser', 'is_bot', 'total_visits', 'total_page_views', 
        'first_visit', 'last_visit'
    ]
    list_filter = [
        'is_bot', 'is_mobile', 'device_type', 'country', 
        'first_visit', 'last_visit'
    ]
    search_fields = ['ip_address', 'country', 'city', 'browser', 'user_agent']
    readonly_fields = [
        'ip_address', 'session_key', 'user_agent', 'browser', 'browser_version',
        'device_type', 'os', 'os_version', 'is_bot', 'is_mobile',
        'country', 'country_code', 'city', 'region', 'latitude', 'longitude',
        'referrer', 'landing_page', 'first_visit', 'last_visit',
        'total_visits', 'total_page_views'
    ]
    date_hierarchy = 'first_visit'
    
    fieldsets = (
        ('Visitor Information', {
            'fields': ('ip_address', 'session_key')
        }),
        ('Browser & Device', {
            'fields': ('user_agent', 'browser', 'browser_version', 
                       'device_type', 'os', 'os_version', 'is_bot', 'is_mobile')
        }),
        ('Location', {
            'fields': ('country', 'country_code', 'city', 'region', 
                       'latitude', 'longitude')
        }),
        ('Traffic Source', {
            'fields': ('referrer', 'landing_page')
        }),
        ('Statistics', {
            'fields': ('first_visit', 'last_visit', 'total_visits', 'total_page_views')
        }),
    )


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    """Admin configuration for PageView model"""
    
    list_display = [
        'url', 'page_title', 'visitor', 'country_code', 
        'device_type', 'method', 'timestamp'
    ]
    list_filter = ['device_type', 'country_code', 'method', 'timestamp']
    search_fields = ['url', 'page_title', 'ip_address', 'visitor__ip_address']
    readonly_fields = [
        'visitor', 'url', 'page_title', 'method', 'timestamp',
        'ip_address', 'user_agent', 'referrer', 'session_key',
        'country_code', 'device_type'
    ]
    date_hierarchy = 'timestamp'
    raw_id_fields = ['visitor']
