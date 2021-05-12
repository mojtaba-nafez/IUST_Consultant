from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.models import UserProfile
from .serializers import *
from django.db.models import Q
import datetime
from django.db import transaction
import time


class ConsultantTimeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            start_date = datetime.datetime.strptime(request.GET['date'], "%Y-%m-%d")
            end_date = start_date.__add__(datetime.timedelta(days=1))
            my_employer_consultant_ids = list(
                ConsultantProfile.my_secretaries.through.objects.values_list("consultantprofile_id").filter(
                    userprofile_id=request.user.id))
            consultant_times = ConsultantTime.objects.select_for_update().filter(
                Q(consultant_id__in=my_employer_consultant_ids + [request.user.id]) | Q(user_id=request.user.id),
                Q(start_date__gte=start_date),
                Q(end_date__lt=end_date))
            with transaction.atomic():
                consultant_times_serializer = ConsultantTimeSerializer(consultant_times, many=True)
                return Response(consultant_times_serializer.data, status=status.HTTP_200_OK)

        except MultiValueDictKeyError as parameter_error:
            return Response({"error": "تاریخ را نفرستاده اید"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as date_format_error:
            return Response({"error": "فرمت تاریخ درست نیست"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if request.data.__contains__('consultant_id'):
                consultant = ConsultantProfile.objects.filter(
                    id=request.data['consultant_id'])
                if len(consultant) == 0:
                    return Response({"error": "مشاوری با این شناسه موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    consultant = consultant[0]
                    if len(ConsultantProfile.my_secretaries.through.objects.filter(consultantprofile_id=consultant.id,
                                                                                   userprofile_id=request.user.id)) == 0:
                        return Response({"error": "شما منشی این مشاور نیستید"}, status=status.HTTP_403_FORBIDDEN)
            else:
                consultant = ConsultantProfile.objects.filter(id=request.user.id)
                if len(consultant) == 0:
                    return Response({"error": "شما مشاور نیستید"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    consultant = consultant[0]

            consultant_time_serializer = ConsultantTimeSerializer(data=request.data)
            if consultant_time_serializer.is_valid():
                consultant_time_serializer.validated_data['consultant'] = consultant
                # TODO check similar consultant times
                if len(ConsultantTime.objects.filter(Q(consultant=consultant), Q(
                        start_date=consultant_time_serializer.validated_data['start_date']) | Q(
                    end_date=consultant_time_serializer.validated_data['end_date']))) != 0:
                    return Response({"error": "شما ساعتی مشابه با این ساعت تعریف کرده اید"},
                                    status=status.HTTP_400_BAD_REQUEST)
                consultant_time = consultant_time_serializer.save()
                return Response(ConsultantTimeSerializer(consultant_time).data, status=status.HTTP_200_OK)
            else:
                return Response({"error": consultant_time_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ConsultantTimeId, ):
        try:
            consultant_time = ConsultantTime.objects.select_for_update().filter(id=ConsultantTimeId).select_related(
                "consultant").select_related('user')
            with transaction.atomic():
                if len(consultant_time) == 0:
                    return Response({"error": "شناسه زمان مشاوره موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    consultant_time = consultant_time[0]
                time.sleep(15)
                if consultant_time.consultant.id != request.user.id and len(
                        ConsultantProfile.my_secretaries.through.objects.filter(
                            consultantprofile_id=consultant_time.consultant.id,
                            userprofile_id=request.user.id)) == 0:
                    return Response({"error": "شما دسترسی به این کار را ندارید"}, status=status.HTTP_403_FORBIDDEN)

                consultant_time_serializer = ConsultantTimeSerializer(consultant_time, data=request.data)
                if consultant_time_serializer.is_valid():
                    if consultant_time.user is not None:
                        # TODO send notification for user and confirm from his/her
                        # TODO staging changes of time
                        return Response({"message": "باید منتظر تایید کاربر رزروکننده بمانید",
                                         "reservatore": {"username": consultant_time.user.username,
                                                         "phone_number": consultant_time.user.phone_number}},
                                        status=status.HTTP_202_ACCEPTED)
                    # TODO check similar consultant times
                    consultant_time_serializer.save()
                    return Response(consultant_time_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": consultant_time_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ConsultantTimeId):
        try:
            consultant_time = ConsultantTime.objects.select_for_update().filter(id=ConsultantTimeId).select_related(
                "consultant").select_related("user")
            with transaction.atomic():
                if len(consultant_time) == 0:
                    return Response({"error": "شناسه زمان مشاوره موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    consultant_time = consultant_time[0]

                if consultant_time.consultant.id != request.user.id and len(
                        ConsultantProfile.my_secretaries.through.objects.filter(
                            consultantprofile_id=consultant_time.consultant.id,
                            userprofile_id=request.user.id)) == 0:
                    return Response({"error": "شما دسترسی به این کار را ندارید"}, status=status.HTTP_403_FORBIDDEN)

                # TODO get lock of consultant time - if user are reserving at now
                if consultant_time.user is None:
                    consultant_time.delete()
                    return Response({}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "این ساعت را کاربری رزرو کرده است. در صورت نیاز باید آن را لغو کنید."},
                                    status=status.HTTP_403_FORBIDDEN)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CancelConsultantTime(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, ConsultantTimeId, ):
        try:
            consultant_time = ConsultantTime.objects.filter(id=ConsultantTimeId).select_related(
                "consultant").select_related("user")
            if len(consultant_time) == 0:
                return Response({"error": "شناسه زمان مشاوره موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                consultant_time = consultant_time[0]

            if consultant_time.user is None:
                return Response({"error": "این ساعت هنوز رزرو نشده است"}, status=status.HTTP_400_BAD_REQUEST)

            if consultant_time.start_date.__sub__(timezone.now()) < datetime.timedelta(minutes=60):
                return Response({"error": "به زمان مشاوره کمتر از 60 دقیقه مانده است"},
                                status=status.HTTP_403_FORBIDDEN)

            if consultant_time.user.id == request.user.id:
                # TODO SEND NOTIFICATION FOR CONSULTANT
                # TODO PUNISH USER
                consultant_time.user = None
                consultant_time.save()
                return Response({}, status=status.HTTP_200_OK)

            if consultant_time.consultant.id != request.user.id and len(
                    ConsultantProfile.my_secretaries.through.objects.filter(
                        consultantprofile_id=consultant_time.consultant.id,
                        userprofile_id=request.user.id)) == 0:
                return Response({"error": "شما دسترسی به این کار را ندارید"}, status=status.HTTP_403_FORBIDDEN)
            else:
                # TODO SEND NOTIFICATION FOR USER
                # TODO PUNISH CONSULTANT
                consultant_time.user = None
                consultant_time.save()
                return Response({}, status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
