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
    path('simple/', views.SimpleQueryView.as_view(), name='simple_query'),
    path('datasets/', views.DatasetsView.as_view(), name='datasets'),
    
    # Test interface
    path('test/', views.test_ui, name='test_ui'),
    path('test-api/', views.test_api, name='test_api'),
    
    # Health check
    path('health/', views.health_check, name='health_check'),
]