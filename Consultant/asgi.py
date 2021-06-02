import os

import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Consultant.settings')
django.setup()
application = get_default_application()
# application = ProtocolTypeRouter({
#     "http": AsgiHandler(),
#     "websocket": TokenAuthMiddlewareStack(
#         URLRouter(
#             chat_room.routing.websocket_urlpatterns
#         )
#     ),
#     # Just HTTP for now. (We can add other protocols later.)
# })
