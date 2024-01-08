from django.urls import re_path

from .consumers import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r'chat/(?P<room>\w+)/$', ChatRoomConsumer.as_asgi()),
]
