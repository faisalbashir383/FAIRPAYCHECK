"""
Core app URL configuration.
"""

from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/calculate/', views.calculate_score_api, name='calculate_score'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml'), name='sitemap'),
]
