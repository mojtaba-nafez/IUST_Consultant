from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .serializers import *
from User.models import ConsultantProfile, UserProfile, BaseUser
from message.models import DirectMessage


def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })


class ConnectedUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_id = request.user.id
            # users = DirectMessage.objects.filter(Q(sender__id=user_id) | Q(reciever__id=user_id)).order_by('sender').distinct('sender').order_by('reciever').distinct('reciever').order_by('-date')

            sender = DirectMessage.objects.filter(Q(reciever__id=user_id)).values_list('sender').distinct().values_list(
                'sender', 'date')
            receiver = DirectMessage.objects.filter(Q(sender__id=user_id)).values_list(
                'reciever').distinct().values_list('reciever', 'date')
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

    def get(self, request, UserID, format=None):
        try:
            me = request.user
            messages = DirectMessage.objects.filter(
                (Q(sender=me) & Q(reciever__id=UserID)) | (Q(sender__id=UserID) & Q(reciever__id=me.id))).order_by(
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


