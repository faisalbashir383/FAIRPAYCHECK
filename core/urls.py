"""
Core app URL configuration.
"""

from django.urls import path
from django.views.generic import TemplateView
from django.http import FileResponse
from django.conf import settings
import os
from . import views


def favicon_view(request):
    """Serve favicon.ico directly without redirect."""
    favicon_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'favicon.ico')
    return FileResponse(open(favicon_path, 'rb'), content_type='image/x-icon')


urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/calculate/', views.calculate_score_api, name='calculate_score'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml'), name='sitemap'),
    path('favicon.ico', favicon_view, name='favicon'),
]


