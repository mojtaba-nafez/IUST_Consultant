from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .serializers import *
from User.models import ConsultantProfile, UserProfile, BaseUser
from message.models import ChatMessage


def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })


class ChatMessageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            chat_message_serializer = ChatMessageSerializer(data=request.data)
            if chat_message_serializer.is_valid():
                receiver = BaseUser.objects.filter(username=chat_message_serializer.validated_data['receiver_username'])
                if len(receiver) == 0:
                    return Response({"error": "شناسه دریافت‌کننده درست نیست"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    receiver = receiver[0]
                if len(ConsultantProfile.objects.filter(
                        Q(id=request.user.id) | Q(username=chat_message_serializer.validated_data['receiver_username']))) == 0:
                    return Response({"error": "یک سمت‌پیام باید مشاور باشد"}, status=status.HTTP_403_FORBIDDEN)
                chat_message_serializer.validated_data['sender'] = request.user
                chat_message_serializer.validated_data['receiver'] = receiver
                return_data = ChatMessageSerializer(chat_message_serializer.save()).data
                return Response(data=return_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": chat_message_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, ChatMessageId):
        try:
            chat_message = ChatMessage.objects.filter(id=ChatMessageId).select_related('sender').select_related(
                'receiver')
            if len(chat_message) == 0:
                return Response({"error": "شناسه‌ی پیام صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                chat_message = chat_message[0]

            if (chat_message.sender is not None and chat_message.sender.username == request.user.username) or (
                    chat_message.receiver is not None and chat_message.receiver.username == request.user.username):
                return Response(ChatMessageSerializer(chat_message).data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "شما دسترسی به این پیام را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ChatMessageId):
        try:
            chat_message = ChatMessage.objects.filter(id=ChatMessageId).select_related('sender').select_related(
                'receiver')
            if len(chat_message) == 0:
                return Response({"error": "شناسه‌ی پیام صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                chat_message = chat_message[0]

            if chat_message.sender is not None and chat_message.sender.username == request.user.username:
                chat_message_serializer = ChatMessageSerializer(chat_message, data=request.data)
                if chat_message_serializer.is_valid():
                    chat_message_serializer.save()
                    return Response("پیام بروز‌شد", status=status.HTTP_200_OK)
                else:
                    return Response({"error": chat_message_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "شما دسترسی به این پیام را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ChatMessageId):
        try:
            chat_message = ChatMessage.objects.filter(id=ChatMessageId).select_related('sender')
            if len(chat_message) == 0:
                return Response({'error': 'شناسه پیام صحیح نیست'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                chat_message = chat_message[0]
            if chat_message.sender.id != request.user.id:
                return Response({"error": "شما دسترسی به این‌کار ندارید"}, status=status.HTTP_403_FORBIDDEN)
            chat_message.delete()
            return Response("پیام حذف شد", status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConnectedUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_id = request.user.id
            # users = DirectMessage.objects.filter(Q(sender__id=user_id) | Q(receiver_id=user_id)).order_by('sender').distinct('sender').order_by('receiver').distinct('receiver').order_by('-date')

            sender = ChatMessage.objects.filter(Q(receiver_id=user_id)).values_list('sender').distinct().values_list(
                'sender', 'date')
            receiver = ChatMessage.objects.filter(Q(sender__id=user_id)).values_list(
                'receiver').distinct().values_list('receiver', 'date')
            connected_users_query_set = [i[0] for i in list(sender.union(receiver).order_by('-date'))]
            connected_users_query_set = list(set(connected_users_query_set))
            connected_users_list = []

            for user_id in connected_users_query_set:
                user = BaseUser.objects.get(id=user_id)
                connected_users_list.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "user_type": user.user_type,
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "avatar": user.avatar.url if user.avatar else None
                    }
                )

            return Response(connected_users_list, status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChannelMessagePagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'


class MessageHistory(APIView, ChannelMessagePagination):
    permission_classes = [IsAuthenticated]

    def get(self, request, UserName, format=None):
        try:
            me = request.user
            print(UserName)
            messages = ChatMessage.objects.filter(
                (Q(sender=me) & Q(receiver__username=UserName)) | (Q(sender__username=UserName) & Q(receiver__id=me.id))).order_by(
                '-date')
            page = self.paginate_queryset(messages, request, view=self)
            if page is not None:
                message_serializer = self.get_paginated_response(DirectMessageSerializer(page,
                                                                                         many=True).data)
            else:
                message_serializer = DirectMessageSerializer(messages, many=True)
            return Response(message_serializer.data, status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
