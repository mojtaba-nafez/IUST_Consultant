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


class LoginAPI(ObtainAuthToken):
    permission_classes = []

    def post(self, request, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                # TODO: WRITE NATIVE QUERY HERE , USERNAME OR EMAIL
                user = BaseUser.objects.filter(username=serializer.validated_data['email_username'])
                if len(user) == 0:
                    user = BaseUser.objects.filter(email=serializer.validated_data['email_username'])
                if len(user) == 0:
                    return Response({'error': 'This user not found'}, status=status.HTTP_400_BAD_REQUEST)
                if user[0].password != serializer.validated_data['password']:
                    return Response({'error': 'The password is not true'}, status=status.HTTP_400_BAD_REQUEST)
                token, created = Token.objects.get_or_create(user=user[0])
                if user[0].user_type == "normal_user":
                    user = UserProfile.objects.filter(baseuser_ptr=user[0])
                    return_data = UserProfileSerializer(user[0])
                else:
                    user = ConsultantProfile.objects.filter(baseuser_ptr=user[0])
                    return_data = ConsultantProfileSerializer(user[0])

                return Response({
                    'token': token.key,
                    'data': return_data.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
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


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr=request.user)
            if len(consultant) != 0:
                consultant_serializer = ConsultantProfileSerializer(consultant[0])
                return Response(consultant_serializer.data, status=status.HTTP_200_OK)
            user = UserProfile.objects.filter(baseuser_ptr=request.user)
            user_serializer = UserProfileSerializer(user[0])
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr=request.user)
            if len(consultant) != 0:
                consultant_serializer = BaseUserSerializer(consultant[0], request.data)
                if consultant_serializer.is_valid():
                    consultant_serializer.save()
                    return Response(consultant_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": consultant_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            user = UserProfile.objects.filter(baseuser_ptr=request.user)
            user_serializer = BaseUserSerializer(user[0], request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnotherUserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = ConsultantProfile.objects.filter(username=username)
            if len(user) != 0:
                user_serializer = ConsultantProfileSerializer(user[0])
            else:
                user = UserProfile.objects.filter(username=username)
                if len(user) == 0:
                    return Response({"error": "کاربری با این نام‌کاربری موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user_serializer = UserProfileSerializer(user[0])
            user_profile = user_serializer.data
            del user_profile['email']
            del user_profile['phone_number']
            return Response(user_profile, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
