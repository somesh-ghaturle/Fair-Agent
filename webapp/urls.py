"""
URL configuration for FAIR-Agent Web Application

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Main FAIR-Agent application
    path('', include('fair_agent_app.urls')),
    
    # API endpoints
    path('api/', include('fair_agent_app.api_urls')),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "FAIR-Agent Administration"
admin.site.site_title = "FAIR-Agent Admin Portal"
admin.site.index_title = "Welcome to FAIR-Agent Administration"