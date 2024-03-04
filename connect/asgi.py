"""
ASGI config for connect project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connect.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from core.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'https': get_asgi_application(),
        'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
