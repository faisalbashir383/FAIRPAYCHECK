"""
Core app URL configuration.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/calculate/', views.calculate_score_api, name='calculate_score'),
]
