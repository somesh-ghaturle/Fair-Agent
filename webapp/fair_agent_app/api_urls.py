"""
API URL configuration for FAIR-Agent application
"""

from django.urls import path
from . import views

app_name = 'fair_agent_api'

urlpatterns = [
    # Query processing APIs
    path('query/process/', views.process_query_api, name='process_query'),
    path('query/history/', views.query_history_api, name='query_history'),
    
    # System status and health
    path('system/status/', views.system_status_api, name='system_status'),
    
    # User feedback
    path('feedback/submit/', views.submit_feedback_api, name='submit_feedback'),
    
    # Additional endpoints for frontend
    path('recent-activity/', views.recent_activity_api, name='recent_activity'),
]