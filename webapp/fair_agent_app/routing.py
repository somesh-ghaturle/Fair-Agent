"""
WebSocket routing for FAIR-Agent application
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/query/(?P<session_id>\w+)/$', consumers.QueryConsumer.as_asgi()),
    re_path(r'ws/metrics/$', consumers.MetricsConsumer.as_asgi()),
]