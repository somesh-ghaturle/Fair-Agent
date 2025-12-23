"""
URL configuration for FAIR-Agent application
"""

from django.urls import path
from . import views
from . import https_views

app_name = 'fair_agent_app'

urlpatterns = [
    # Main interface pages
    path('', views.HomeView.as_view(), name='home'),
    path('query/', views.QueryInterfaceView.as_view(), name='query_interface'),
    path('simple/', views.SimpleQueryView.as_view(), name='simple_query'),
    path('datasets/', views.DatasetsView.as_view(), name='datasets'),
    path('architecture/', views.ArchitectureView.as_view(), name='architecture'),
    path('publication/', views.PublicationView.as_view(), name='publication'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # HTTPS redirect helper
    path('https-info/', https_views.https_redirect_info, name='https_info'),
    
    # Test interface
    path('test/', views.test_ui, name='test_ui'),
    path('test-api/', views.test_api, name='test_api'),
]