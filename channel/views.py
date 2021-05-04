from django.shortcuts import render
import threading

from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView

from User.models import UserProfile
from .serializers import *
from .models import *

create_link_lock = threading.Lock()


def create_uuid_link(thread_lock):
    import uuid
    with thread_lock:
        return uuid.uuid4().hex


class CreateLinkAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            unique_link = create_uuid_link(create_link_lock)
            return Response(data={
                "invite_link": unique_link,
            }, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChannelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, channelId, format=None):
        try:
            channel = Channel.objects.filter(id=channelId).select_related('consultant')
            if len(channel) == 0:
                return Response({"error": "This channel id is not exits"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ChannelSerializer(channel[0]).data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)
            if len(consultant) == 0:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            consultant = consultant[0]
            channel_serializer = ChannelSerializer(data=request.data)
            if channel_serializer.is_valid():
                channel_serializer.validated_data['consultant'] = consultant
                channel = channel_serializer.save()
                channel_serializer = ChannelSerializer(channel)
                return Response(
                    data=channel_serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": channel_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditChannel(APIView):
    #permission_classes = [IsAuthenticated]
    def put(self, request, channelId, format=None):
        try:
            print(request.data)
            
            serializer = EditChannelSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                ch=channel = Channel.objects.filter(id=channelId)

                if ch[0].consultant.id != user.id and ( user not in UserProfile.objects.filter(consultantprofile=ch[0].consultant)):
                    return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)

                name = serializer.data.get('name')
                print(serializer.data)
                if name!=None:
                    Channel.objects.filter(pk=channelId).update(name=name)
                invite_link = serializer.data.get('invite_link')
                if invite_link:
                    try:
                        Channel.objects.filter(pk=channelId).update(invite_link=invite_link)
                    except:
                        pass
                    
                try:
                    avatar =  request.FILES['avatar']
                    ch = Channel.objects.get(pk=channelId)
                    ch.avatar.delete(save=True)
                    ch.avatar = avatar
                    ch.save()
                except:
                    pass

                description = serializer.data.get('description')
                if description:
                    Channel.objects.filter(pk=channelId).update(description=description)
                
                return Response({'status': 'OK'},
                                    status=status.HTTP_200_OK)


        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                




