from django.shortcuts import render

from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
import datetime
import re

def date_validator(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

class Reserve(APIView):
    Authenticated =[IsAuthenticated]
    #  all date are in tzinfo=<UTC>
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
    def get(self, request, ConsultantID, format=None):
        try:
            date = request.GET['date']
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                start_day = date + " 00:00:00+00:00"
                end_day = date + " 23:59:59+00:00"
            except ValueError:
                return Response("Incorrect date format, should be YYYY-MM-DD", status=status.HTTP_400_BAD_REQUEST)
            consultant_time=ConsultantTime.objects.filter(consultant__id=ConsultantID, start_date__gte=start_day, start_date__lte=end_day)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "+00:00"

            
            obsolete_filled_time = consultant_time.exclude(user=None, end_date__gt=current_time)
            obsolete_empty_time = consultant_time.exclude(end_date__gt=current_time).filter(user=None)

            empty_time = consultant_time.exclude(start_date__lt=current_time).filter(user=None)
            filled_time = consultant_time.exclude(start_date__lt=current_time, user=None)
            print("herrrreeee")
            data = {
                "obsolete_reserved_time":[],
                "obsolete_empty_time":[],
                "empty_time":[],
                "reserved_time":[],
            }


            for i in range(len(obsolete_filled_time)):
                obj=obsolete_filled_time[i]
                data["obsolete_reserved_time"].append({
                        "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute,obj.start_date.second),
                        "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                })
            for i in range(len(obsolete_empty_time)):
                obj=obsolete_empty_time[i]
                data["obsolete_empty_time"].append({
                        "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute,obj.start_date.second),
                        "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                })
            for i in range(len(empty_time)):
                obj=empty_time[i]
                data["empty_time"].append({
                        "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute,obj.start_date.second),
                        "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                })
            for i in range(len(filled_time)):
                obj=filled_time[i]
                data["reserved_time"].append({
                        "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute,obj.start_date.second),
                        "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                })

            print(data)

            return Response({"data":data}, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
