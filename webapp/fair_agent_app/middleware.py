"""
Custom middleware for FAIR-Agent Web Application
"""

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class HTTPSRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to handle HTTPS requests and redirect them to HTTP for development server
    """
    
    def process_request(self, request):
        """
        Process incoming requests and handle HTTPS to HTTP conversion
        """
        # Check if the request is coming via HTTPS
        if request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https':
            logger.info("HTTPS request detected, redirecting to HTTP")
            
            # Get the current URL
            host = request.get_host()
            path = request.get_full_path()
            
            # Create HTTP URL
            http_url = f"http://{host}{path}"
            
            # Redirect to HTTP version
            return HttpResponsePermanentRedirect(http_url)
        
        return None

class DevelopmentSecurityMiddleware(MiddlewareMixin):
    """
    Custom security middleware for development that prevents browser HTTPS forcing
    """
    
    def process_response(self, request, response):
        """
        Process response to add headers that prevent HTTPS enforcement
        """
        if hasattr(response, 'headers'):
            # Remove any HSTS headers that might force HTTPS
            response.headers.pop('Strict-Transport-Security', None)
            
            # Add headers to indicate HTTP is acceptable
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # Explicitly set that HTTPS is NOT required
            response.headers['X-HTTPS-Required'] = 'false'
            
        return response