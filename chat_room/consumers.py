import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.exceptions import StopConsumer


class DirectConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room_group_name = None

    def connect(self):
        self.accept()
        # check user is not AnonymousUser
        # if isinstance(self.scope['user'], AnonymousUser):
        #     self.send_json(content={
        #         "message": "شما باید ابتدا وارد حساب کاربری خود شوید",
        #         "type": "error"
        #     })
        #     self.close()
        #     raise StopConsumer()
        # else:
        #     self.user = self.scope['user']
        room_name = self.scope['url_route']['kwargs']['RoomName']
        # room_usernames = room_name.split('-')
        # if self.user.username not in room_usernames:
        #     self.send_json(content={
        #         "message": "اسم گروه صحیح نیست",
        #         "type": "error"
        #     })
        #     self.close()
        #     raise StopConsumer()
        self.room_group_name = 'direct-%s' % room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive_json(self, content, **kwargs):
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,             {
                'type': 'chat_message',
                'message': content
            })

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send_json(content=event['message'])
