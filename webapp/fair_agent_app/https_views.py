"""
Custom views for handling HTTPS to HTTP redirects
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def https_redirect_info(request):
    """
    Provide information about HTTPS to HTTP redirect
    """
    logger.info(f"HTTPS redirect info requested from {request.META.get('HTTP_HOST', 'unknown')}")
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FAIR-Agent - HTTP Required</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #e3f2fd, #f0f8ff);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                max-width: 500px;
                text-align: center;
            }
            .icon {
                font-size: 3rem;
                color: #007bff;
                margin-bottom: 1rem;
            }
            h1 {
                color: #333;
                margin-bottom: 1rem;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 1rem;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🔒➡️🌐</div>
            <h1>HTTPS → HTTP Redirect</h1>
            <p>The FAIR-Agent development server only supports HTTP connections.</p>
            <p>Please use the HTTP version of the URL:</p>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
                <strong>http://127.0.0.1:8000/</strong>
            </div>
            <a href="http://127.0.0.1:8000/" class="btn">Go to FAIR-Agent (HTTP)</a>
            <div style="margin-top: 2rem; font-size: 0.9rem; color: #666;">
                <p><strong>Why HTTP?</strong></p>
                <p>Django's development server is designed for local development and testing. 
                For production deployments, HTTPS would be properly configured with SSL certificates.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_content, content_type='text/html')