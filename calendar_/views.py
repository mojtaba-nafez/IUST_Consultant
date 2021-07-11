from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage

from User.models import UserProfile
from .serializers import *
from django.db.models import Q
import datetime
from django.db import transaction
import time


class Reserve(APIView):
    Authenticated = [IsAuthenticated]

    #  all date are in tzinfo=<UTC>
    def post(self, request, ConsultantID, format=None):
        try:
            serializer = ReserveConsultantTimeSerializer(data=request.data)
            if serializer.is_valid():
                '''
                consultant_time = ConsultantTime.objects.filter(consultant__id=ConsultantID)

                if len(consultant_time) == 0:
                    return Response("this consultant has no empty time.", status=status.HTTP_404_NOT_FOUND)
                start_date = serializer.data.get('start_date')
                start_date = str(start_date).replace('Z', '+00:00')
                start_date = str(start_date).replace('T', ' ')

                end_date = serializer.data.get('end_date')
                end_date = str(end_date).replace('Z', '+00:00')
                end_date = str(end_date).replace('T', ' ')
                print(end_date)
                consultant_time = ConsultantTime.objects.filter(consultant__id=ConsultantID, user=None,
                                                                start_date=start_date, end_date=end_date)
                for i in range(len(consultant_time)):
                    print(consultant_time[i].end_date)

                if len(consultant_time) == 0:
                    return Response("this consultant is busy in this time.", status=status.HTTP_404_NOT_FOUND)
                '''
                consultant_time = ConsultantTime.objects.filter(consultant__id=ConsultantID)
                if len(consultant_time) == 0:
                    return Response(" مشاور زمانی برای مشاوره ندارد!", status=status.HTTP_400_BAD_REQUEST)
                
                consultant_time = ConsultantTime.objects.filter(id=request.data['id'])
                if len(consultant_time) == 0:
                    return Response("چنین زمانی برای مشاوره وجود ندارد.!", status=status.HTTP_400_BAD_REQUEST)
                
                if consultant_time[0].user!=None:
                    return Response("متاسفانه این زمان قبلا پر شده است!", status=status.HTTP_400_BAD_REQUEST)
                


                ConsultantTime.objects.filter(id=consultant_time[0].id).update(user=request.user.id,
                                                                               title=serializer.data.get('title'),
                                                                               description=serializer.data.get(
                                                                                   'description'))
                email_subject="زمان مشاوره"
                temp_time=consultant_time[0].start_date
                email_body=' شما در تاریخ ' + str(temp_time.year)+'/'+str(temp_time.month) + '/' + str(temp_time.day) + ' در ساعت '+ str(temp_time.hour)+':'+str(temp_time.minute) + ':' + str(temp_time.second) + ' برای مشاوره با آقای ' + str(consultant_time[0].consultant.first_name +' '+consultant_time[0].consultant.last_name) + ' با موفقیت زمان رزرو کردید.'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [request.user.email],
                )
                email.send(fail_silently=False)

                return Response(data={"status": "ok"}, status=status.HTTP_200_OK)
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
            consultant_time = ConsultantTime.objects.filter(consultant__id=ConsultantID, start_date__gte=start_day,
                                                            start_date__lte=end_day)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "+00:00"

            obsolete_filled_time = consultant_time.exclude(start_date__gt=current_time).exclude(user=None)
            obsolete_empty_time = consultant_time.exclude(start_date__gt=current_time).filter(user=None)

            empty_time = consultant_time.exclude(start_date__lt=current_time).filter(user=None)
            filled_time = consultant_time.exclude(start_date__lt=current_time).exclude(user=None)

            data = {
                "obsolete_reserved_time": [],
                "obsolete_empty_time": [],
                "empty_time": [],
                "reserved_time": [],
            }
            for i in range(len(obsolete_filled_time)):
                obj = obsolete_filled_time[i]
                data["obsolete_reserved_time"].append({
                    "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute, obj.start_date.second),
                    "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                    "id": obj.id,
                })
            for i in range(len(obsolete_empty_time)):
                obj = obsolete_empty_time[i]
                data["obsolete_empty_time"].append({
                    "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute, obj.start_date.second),
                    "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                    "id": obj.id,
                })
            for i in range(len(empty_time)):
                obj = empty_time[i]
                data["empty_time"].append({
                    "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute, obj.start_date.second),
                    "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                    "id": obj.id,
                })
            for i in range(len(filled_time)):
                obj = filled_time[i]
                data["reserved_time"].append({
                    "start_time": datetime.time(obj.start_date.hour, obj.start_date.minute, obj.start_date.second),
                    "end_time": datetime.time(obj.end_date.hour, obj.end_date.minute, obj.end_date.second),
                    "id": obj.id,
                })
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                same_consultant_time = ConsultantTime.objects.filter(Q(consultant=consultant), Q(
                    start_date__lte=consultant_time_serializer.validated_data['start_date'],
                    end_date__gt=consultant_time_serializer.validated_data['start_date']) | Q(
                    start_date__lt=consultant_time_serializer.validated_data['end_date'],
                    end_date__gte=consultant_time_serializer.validated_data['end_date']) | Q(
                    start_date__gte=consultant_time_serializer.validated_data['start_date'],
                    start_date__lt=consultant_time_serializer.validated_data['end_date']) | Q(
                    end_date__gt=consultant_time_serializer.validated_data['start_date'],
                    end_date__lte=consultant_time_serializer.validated_data['end_date']))
                if len(same_consultant_time) != 0:
                    return Response({"error": "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                                     "consultant_time_id": same_consultant_time[0].id},
                                    status=status.HTTP_400_BAD_REQUEST)
                consultant_time = consultant_time_serializer.save()
                return Response(ConsultantTimeSerializer(consultant_time).data, status=status.HTTP_200_OK)
            else:
                return Response({"error": consultant_time_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ConsultantTimeId, ):
        try:
            consultant_time = ConsultantTime.objects.select_for_update().filter(id=ConsultantTimeId)
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

                consultant_time_serializer = ConsultantTimeSerializer(consultant_time, data=request.data)
                if consultant_time_serializer.is_valid():
                    if consultant_time.user is not None:
                        # TODO send notification for user and confirm from his/her
                        # TODO staging changes of time
                        return Response({"message": "باید منتظر تایید کاربر رزروکننده بمانید",
                                         "reservatore": {"username": consultant_time.user.username,
                                                         "phone_number": consultant_time.user.phone_number}},
                                        status=status.HTTP_202_ACCEPTED)
                    same_consultant_time = ConsultantTime.objects.filter(
                        ~Q(id=consultant_time.id), Q(consultant=consultant_time.consultant), Q(
                            start_date__lte=consultant_time_serializer.validated_data['start_date'],
                            end_date__gt=consultant_time_serializer.validated_data['start_date']) | Q(
                            start_date__lt=consultant_time_serializer.validated_data['end_date'],
                            end_date__gte=consultant_time_serializer.validated_data['end_date']) | Q(
                            start_date__gte=consultant_time_serializer.validated_data['start_date'],
                            start_date__lt=consultant_time_serializer.validated_data['end_date']) | Q(
                            end_date__gt=consultant_time_serializer.validated_data['start_date'],
                            end_date__lte=consultant_time_serializer.validated_data['end_date']))
                    if len(same_consultant_time) != 0:
                        return Response({"error": "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                                         "consultant_time_id": same_consultant_time[0].id},
                                        status=status.HTTP_400_BAD_REQUEST)
                    consultant_time_serializer.save()
                    return Response(consultant_time_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": consultant_time_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ConsultantTimeId):
        try:
            consultant_time = ConsultantTime.objects.select_for_update().filter(id=ConsultantTimeId)
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


def update_consultant_time(consultant_time, user_grade, user_comment):
    consultant_time.user_grade = user_grade
    consultant_time.user_comment = user_comment
    consultant_time.user_grade_date = timezone.now()
    consultant_time.save()


def update_consultant_satisfaction(consultant, user_grade):
    old_consultant_satisfaction = (consultant.satisfaction_percentage / 20) * consultant.count_of_all_comments
    new_consultant_satisfaction = old_consultant_satisfaction + user_grade
    consultant.count_of_all_comments += 1
    new_consultant_satisfaction_percentage = int(new_consultant_satisfaction / consultant.count_of_all_comments * 20)
    consultant.satisfaction_percentage = new_consultant_satisfaction_percentage
    ConsultantProfile.objects.filter(id=consultant.id).update(
        count_of_all_comments = consultant.count_of_all_comments,
        satisfaction_percentage = consultant.satisfaction_percentage
    )


class CommentAndGradPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"


class CommentAndGradeAPI(APIView, CommentAndGradPagination):
    permission_classes = [IsAuthenticated]

    def post(self, request, ConsultantTimeId):
        try:
            consultant_time = ConsultantTime.objects.filter(id=ConsultantTimeId).select_related("user")
            if len(consultant_time) == 0:
                return Response({"error": "شناسه‌ی زمان‌مشاوره صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                consultant_time = consultant_time[0]
            if consultant_time.user is None or consultant_time.user.id != request.user.id:
                return Response({"error": "شما مجاز به این کار نیستید"}, status=status.HTTP_403_FORBIDDEN)
            comment_and_grade_serializer = CommentAndRateSerializer(data=request.data)
            if comment_and_grade_serializer.is_valid():
                update_consultant_time(consultant_time, comment_and_grade_serializer.validated_data['user_grade'],
                                       comment_and_grade_serializer.validated_data['user_comment'])
                update_consultant_satisfaction(consultant_time.consultant, int(consultant_time.user_grade))
                return Response("OK", status=status.HTTP_200_OK)
            else:
                return Response({"error": comment_and_grade_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, ConsultantUsername):
        try:
            consultant = ConsultantProfile.objects.filter(username=ConsultantUsername)
            if len(consultant) == 0:
                return Response({"error": "شناسه‌ی مشاور صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                consultant = consultant[0]
            consultant_times = ConsultantTime.objects.filter(consultant__username=ConsultantUsername,
                                                             user_grade__isnull=False).order_by('-user_grade_date')
            page = self.paginate_queryset(consultant_times, request, view=self)
            if page is not None:
                consultant_times_serializer = self.get_paginated_response(CommentAndRateSerializer(page,
                                                                                                  many=True).data)
            else:
                consultant_times_serializer = CommentAndRateSerializer(consultant_times, many=True)
            consultant_times_serializer.data['count_of_all_comments'] = consultant.count_of_all_comments
            consultant_times_serializer.data['satisfaction_percentage'] = consultant.satisfaction_percentage
            return Response(consultant_times_serializer.data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response({"error": server_error.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
