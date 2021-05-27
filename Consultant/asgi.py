import os

import django
import chat_room.routing
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter

from Consultant.token_auth import TokenAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Consultant.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": TokenAuthMiddlewareStack(
    URLRouter(
      chat_room.routing.websocket_urlpatterns
    )
  ),
  # Just HTTP for now. (We can add other protocols later.)
})