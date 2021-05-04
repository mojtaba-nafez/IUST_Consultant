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

