from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class ConsultantTime(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.data.__contains__('consultant_id'):
                consultant = ConsultantProfile.objects.filter(
                    id=request.data['consultant_id'])
                if len(consultant) == 0:
                    return Response({"error": "مشاوری با این شناسه موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    consultant = consultant[0]
                    secretary = UserProfile.objects.filter(baseuser_ptr=request.user)[0]
                    if len(ConsultantProfile.my_secretaries.through.objects.filter(consultantprofile=consultant,
                                                                                   userprofile=secretary)) == 0:
                        return Response({"error": "شما منشی این مشاور نیستید"}, status=status.HTTP_403_FORBIDDEN)
            else:
                consultant = ConsultantProfile.objects.filter(baseuser_ptr=request.user)
                if len(consultant) == 0:
                    return Response({"error": "شما مشاور نیستید"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    consultant = consultant[0]

            consultant_time_serializer = ConsultantTimeSerializer(data=request.data)
            if consultant_time_serializer.is_valid():
                consultant_time_serializer.validated_data['consultant'] = consultant
                consultant_time = consultant_time_serializer.save()
                return Response(ConsultantTimeSerializer(consultant_time).data, status=status.HTTP_200_OK)
            else:
                return Response({"error": consultant_time_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
