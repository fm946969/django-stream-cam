# chat/routing.py
from django.urls import re_path

from . import FirstConsumer

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', FirstConsumer.FirstConsumer.as_asgi()),
    re_path('ws/cam/', FirstConsumer.FirstConsumer.as_asgi()),
]