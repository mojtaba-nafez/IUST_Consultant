from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView

from User.models import ConsultantProfile
from .serializers import *


class ChannelMessagePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class ChannelMessageAPI(APIView, ChannelMessagePagination):
    permission_classes = [IsAuthenticated]

    def get(self, request, channelId, format=None):
        try:
            channel = Channel.objects.filter(id=channelId)
            if len(channel) == 0:
                return Response({"error": "شناسه کانال موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
            messages = ChannelMessage.objects.filter(channel_id=channel[0].id).order_by('-date')
            page = self.paginate_queryset(messages, request, view=self)
            if page is not None:
                message_serializer = self.get_paginated_response(ChannelMessageSerializer(page,
                                                                                          many=True).data)
            else:
                message_serializer = ChannelMessageSerializer(messages, many=True)
            return Response(message_serializer.data, status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, channelId, format=None):
        try:
            message_serializer = ChannelMessageSerializer(data=request.data)
            if message_serializer.is_valid():
                channel = Channel.objects.filter(id=channelId).select_related(
                    'consultant')
                if len(channel) == 0:
                    return Response({"error": "شناسه کانال موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
                message_creator = request.user
                if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
                        ConsultantProfile.my_secretaries.through.objects.filter(
                            consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
                    return Response({"error": "شما مجوز انجام این کار را ندارید"},
                                    status=status.HTTP_403_FORBIDDEN)
                message_serializer.validated_data['creator'] = message_creator
                message_serializer.validated_data['channel'] = channel[0]
                message = message_serializer.save()
                message_serializer = ChannelMessageSerializer(message)
                return Response(message_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": message_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, channelId, messageId, format=None):
        try:
            message_serializer = ChannelMessageSerializer(data=request.data)
            if message_serializer.is_valid():
                message = ChannelMessage.objects.filter(
                    id=messageId).select_related('channel')
                if len(message) == 0:
                    return Response({"error": "شناسه‌ی پیام صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
                channel = Channel.objects.filter(id=channelId).select_related(
                    'consultant')
                if len(channel) == 0:
                    return Response({"error": "شناسه‌ی کانال صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
                if message[0].channel.id != channel[0].id:
                    return Response({"error": "شناسه‌ی کانال و پیام با هم مطابقت ندارد"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
                        ConsultantProfile.my_secretaries.through.objects.filter(
                            consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
                    return Response({"error": "شما مجوز چنین کاری را ندارید"},
                                    status=status.HTTP_403_FORBIDDEN)
                message_serializer = ChannelMessageSerializer(message[0], data=message_serializer.validated_data)
                if message_serializer.is_valid(raise_exception=True):
                    message_serializer.save()
                    return Response(message_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": message_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, channelId, messageId, format=None):
        try:
            message = ChannelMessage.objects.filter(
                id=messageId).select_related('channel')
            if len(message) == 0:
                return Response({"error": "شناسه‌ی پیام صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
            channel = Channel.objects.filter(id=channelId).select_related(
                'consultant')
            if len(channel) == 0:
                return Response({"error": "شناسه‌ی کانال صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
            if message[0].channel.id != channel[0].id:
                return Response({"error": "شناسه‌ی کانال و پیام با هم مطابقت ندارد"},
                                status=status.HTTP_400_BAD_REQUEST)
            if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
                    ConsultantProfile.my_secretaries.through.objects.filter(
                        consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
                return Response({"error": "شما مجوز چنین کاری را ندارید"},
                                status=status.HTTP_403_FORBIDDEN)

            message.delete()
            return Response("پیام حذف شد", status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
