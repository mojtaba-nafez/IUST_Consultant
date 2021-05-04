from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from channel.models import Channel
from .serializers import *
from django.views.generic import TemplateView

from .models import *


class SwaggerUI(TemplateView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'swagger-ui.html')


class UserSignupAPI(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        try:
            user_serializer = UserProfileSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'data': user_serializer.validated_data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConsultantSignupAPI(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        try:
            consultant_serializer = ConsultantProfileSerializer(data=request.data)
            if consultant_serializer.is_valid():
                user = consultant_serializer.save()
                consultant_serializer = ConsultantProfileSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'data': consultant_serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': consultant_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
