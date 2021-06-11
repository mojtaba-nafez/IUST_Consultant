from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from calendar_.models import ConsultantTime

API_KEY = "YOUR_API_KEY"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


class ChatVideoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ConsultantTimeId):
        try:
            consultant_time = ConsultantTime.objects.filter(id=ConsultantTimeId).select_related(
                'consultant').select_related('user')
            if len(consultant_time) == 0:
                return Response({"error": "شناسه‌ی زمان‌مشاوره صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                consultant_time = consultant_time[0]
            if consultant_time.user is None or consultant_time.consultant is None:
                return Response({"error": "دسترسی به این زمان‌مشاوره را ندارید"}, status=status.HTTP_403_FORBIDDEN)
            if consultant_time.user.id != request.user.id and consultant_time.consultant.id != request.user.id:
                return Response({"error": "دسترسی به این زمان‌مشاوره را ندارید"}, status=status.HTTP_403_FORBIDDEN)
            if consultant_time.start_date < timezone.now():
                return Response({"error": "زمان مشاوره فرانرسیده‌است"}, status=status.HTTP_403_FORBIDDEN)
            if consultant_time.end_date > timezone.now():
                return Response({"error": "زمان مشاوره به‌اتمام رسیده‌است"}, status=status.HTTP_403_FORBIDDEN)

        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
