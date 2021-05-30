from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<RoomName>\w+)/$', consumers.DirectConsumer.as_asgi()),
]