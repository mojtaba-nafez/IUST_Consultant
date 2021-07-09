import pytz
import datetime
import requests
from django.shortcuts import render
from django.utils import timezone
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from calendar_.models import ConsultantTime

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmFwcGVhci5pbiIsImF1ZCI6Imh0dHBzOi8vYXBpLmFwcGVhci5pbi92MSIsImV4cCI6OTAwNzE5OTI1NDc0MDk5MSwiaWF0IjoxNjI1ODM3MTAwLCJvcmdhbml6YXRpb25JZCI6MTE5Mzk0LCJqdGkiOiJjMmQ2NDVmNC1iZDBmLTQ2MmQtYjgyOC0wNDZiMjM1MWQwOTgifQ.k9wzezLcbGFvI1XW3rg5ZnJLUo1PlGjziNh9gpBFSNE"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def check_video_room_conditions(consultant_time, request):
    if len(consultant_time) == 0:
        return False, Response({"error": "شناسه‌ی زمان‌مشاوره صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        consultant_time = consultant_time[0]
    # if consultant_time.user is None or consultant_time.consultant is None:
    #     return False, Response({"error": "این زمان رزرو نشده است"}, status=status.HTTP_403_FORBIDDEN)
    # if consultant_time.user.id != request.user.id and consultant_time.consultant.id != request.user.id:
    #     return False, Response({"error": "دسترسی به این زمان‌مشاوره را ندارید"}, status=status.HTTP_403_FORBIDDEN)
    if consultant_time.end_date < timezone.now():
        return False, Response({"error": "زمان مشاوره به‌اتمام رسیده‌است"}, status=status.HTTP_400_BAD_REQUEST)
    if consultant_time.start_date > timezone.now():
        return False, Response({"error": "زمان مشاوره فرانرسیده‌است"}, status=status.HTTP_400_BAD_REQUEST)
    return True, None


def create_whereby_room(consultant_time):
    data = {
        "startDate": (consultant_time.start_date - datetime.timedelta(minutes=5)).__str__(),
        "endDate": (consultant_time.end_date + datetime.timedelta(minutes=5)).__str__(),
        "fields": ["hostRoomUrl"],
    }
    whereby_response = requests.post(
        "https://api.whereby.dev/v1/meetings",
        headers=headers,
        json=data
    )
    return whereby_response


class ChatVideoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ConsultantTimeId):
        try:
            consultant_time = ConsultantTime.objects.filter(id=ConsultantTimeId).select_related(
                'consultant').select_related('user')
            pass_conditions, response = check_video_room_conditions(consultant_time, request)
            if not pass_conditions:
                return response
            else:
                consultant_time = consultant_time[0]
            if consultant_time.whereby_meeting_id is None:
                whereby_response = create_whereby_room(consultant_time)
                whereby_response_data = json.loads(whereby_response.text)
                if whereby_response.status_code == status.HTTP_201_CREATED:
                    consultant_time.whereby_meeting_id = int(whereby_response_data["meetingId"])
                    consultant_time.whereby_room_url = whereby_response_data['roomUrl']
                    consultant_time.whereby_host_room_url = whereby_response_data['hostRoomUrl']
                    consultant_time.save()
                else:
                    return Response(whereby_response_data, status=whereby_response.status_code)
            data = {
                "meetingId": consultant_time.whereby_meeting_id,
                "roomUrl": consultant_time.whereby_room_url,
                "hostRoomUrl": consultant_time.whereby_host_room_url if consultant_time.consultant.id == request.user.id else None,
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
