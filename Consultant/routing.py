from channels.http import AsgiHandler
from channels.routing import URLRouter, ProtocolTypeRouter
from django.urls import re_path

from Consultant.token_auth import TokenAuthMiddlewareStack
from chat_room import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<RoomName>\w+)/$', consumers.DirectConsumer.as_asgi()),
]
application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})