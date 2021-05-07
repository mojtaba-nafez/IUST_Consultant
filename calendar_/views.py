from django.shortcuts import render

from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *

class Reserve(APIView):
    #Authenticated =[IsAuthenticated]
    def post(self, request, ConsultantID, format=None):
        try:
            ReserveConsultantTimeSerializer(data=request.data)
            print("fddf")
            

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

