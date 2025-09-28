#!/usr/bin/env python3
"""
Django-based Web Application for FAIR-Agent System

This module creates a web interface for the FAIR-Agent multi-agent framework,
allowing users to interact with the system through a user-friendly web interface.

Features:
- Query submission and response display
- Real-time FAIR metrics visualization
- Agent performance monitoring
- Safety protocol enforcement
- Multi-domain query handling
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path to import FAIR-Agent modules
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()