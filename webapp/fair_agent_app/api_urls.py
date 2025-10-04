"""
API URL configuration for FAIR-Agent application
CS668 Analytics Capstone - Fall 2025
"""

from django.urls import path
from . import views, model_api

app_name = 'fair_agent_api'

urlpatterns = [
    # Query processing APIs
    path('query/process/', views.process_query_api, name='process_query'),
    path('query/history/', views.query_history_api, name='query_history'),
    
    # System status and health
    path('system/status/', views.system_status_api, name='system_status'),
    
    # User feedback
    path('feedback/submit/', views.submit_feedback_api, name='submit_feedback'),
    
    # Model management APIs (New for CS668 project)
    path('models/available/', model_api.get_available_models, name='available_models'),
    path('models/load/', model_api.load_model, name='load_model'),
    path('models/unload/', model_api.unload_model, name='unload_model'),
    path('models/capabilities/', model_api.get_model_capabilities, name='model_capabilities'),
    path('models/benchmark/', model_api.benchmark_models, name='benchmark_models'),
    path('models/test/', model_api.test_model_response, name='test_model'),
    
    # Additional endpoints for frontend
    path('recent-activity/', views.recent_activity_api, name='recent_activity'),
]