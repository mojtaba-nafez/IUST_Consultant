from django.shortcuts import render

from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
import datetime

class Reserve(APIView):
    Authenticated =[IsAuthenticated]
    def post(self, request, ConsultantID, format=None):
        try:
            serializer = ReserveConsultantTimeSerializer(data=request.data)
            if serializer.is_valid():
                consultant_time=ConsultantTime.objects.filter(consultant__id=ConsultantID)

                if len(consultant_time)==0:
                    return Response("this consultant has no empty time.", status=status.HTTP_404_NOT_FOUND)
                start_date=serializer.data.get('start_date')
                start_date=str(start_date).replace('Z', '+00:00')
                start_date=str(start_date).replace('T', ' ')
                
                end_date=serializer.data.get('end_date') 
                end_date=str(end_date).replace('Z', '+00:00')
                end_date=str(end_date).replace('T', ' ')
                print(end_date)
                consultant_time=ConsultantTime.objects.filter(consultant__id=ConsultantID, user=None, start_date=start_date, end_date=end_date)
                for i in range(len(consultant_time)):
                    print(consultant_time[i].end_date)
                
                if len(consultant_time)==0: 
                    return Response("this consultant is busy in this time.", status=status.HTTP_404_NOT_FOUND)

                ConsultantTime.objects.filter(id=consultant_time[0].id).update(user=request.user.id, title=serializer.data.get('title'), description=serializer.data.get('description'))

                return Response(data={ "status": "ok"}, status=status.HTTP_200_OK)
            return Response({'status': 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

