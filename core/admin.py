from django.contrib import admin
from .models import VisitorLog, PageView, BlogPost, Author


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


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin configuration for BlogPost model"""
    
    list_display = ['title', 'slug', 'author', 'is_published', 'published_at', 'updated_at']
    list_filter = ['is_published', 'published_at', 'author']
    search_fields = ['title', 'slug', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    raw_id_fields = ['author']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Featured Image', {
            'fields': ('featured_image',),
            'description': 'Use GitHub raw URL for image (1200x630)'
        }),
        ('Author', {
            'fields': ('author',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration for Author model"""
    
    list_display = ['name', 'slug', 'linkedin_url']
    search_fields = ['name', 'slug', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Identity', {
            'fields': ('name', 'slug', 'profile_image')
        }),
        ('Bio & Expertise', {
            'fields': ('bio', 'expertise'),
            'description': 'Human-written bio and comma-separated expertise areas'
        }),
        ('External Links (E-E-A-T)', {
            'fields': ('linkedin_url', 'github_url'),
            'description': 'LinkedIn is mandatory for Google Discover eligibility'
        }),
    )

