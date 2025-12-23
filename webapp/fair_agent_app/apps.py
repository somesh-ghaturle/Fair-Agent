"""
Django app configuration for FAIR-Agent application
"""

import os
from django.apps import AppConfig


class FairAgentAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fair_agent_app'
    verbose_name = 'FAIR-Agent Application'
    
    def ready(self):
        """
        Initialize FAIR-Agent system when Django starts
        """
        try:
            # Django's autoreloader can call AppConfig.ready() twice.
            # Only initialize the service in the reloader child process.
            if os.environ.get('RUN_MAIN') != 'true':
                return

            from .services import FairAgentService
            # Initialize the FAIR-Agent service
            FairAgentService.initialize()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to initialize FAIR-Agent service: {e}")