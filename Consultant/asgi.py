import os

from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Consultant.settings')
channel_layer = get_channel_layer()
# django.setup()

# application = ProtocolTypeRouter({
#     "http": get_wsgi_application(),
#     "websocket": TokenAuthMiddlewareStack(
#         URLRouter(
#             chat_room.routing.websocket_urlpatterns
#         )
#     ),
#     # Just HTTP for now. (We can add other protocols later.)
# })
