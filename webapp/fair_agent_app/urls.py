"""
URL configuration for FAIR-Agent application
"""

from django.urls import path
from . import views

app_name = 'fair_agent_app'

urlpatterns = [
    # Main interface pages
    path('', views.HomeView.as_view(), name='home'),
    path('query/', views.QueryInterfaceView.as_view(), name='query_interface'),
    
    # Health check
    path('health/', views.health_check, name='health_check'),
]