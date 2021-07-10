from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from User.models import UserProfile
from .serializers import *


class ApplicantRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def create_secretary_request(self, request):
        channel = Channel.objects.filter(consultant__username=request.user.username)
        if len(channel) == 0:
            return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
        request_serializer = SecretaryRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            if request.user.username == request_serializer.validated_data['target_user']:
                return Response({"error": "Target username is you!!!"}, status=status.HTTP_400_BAD_REQUEST)
            recipient_request = UserProfile.objects.filter(username=request_serializer.validated_data['target_user'])
            if len(recipient_request) == 0:
                return Response({"error": "Target username is not valid"}, status=status.HTTP_400_BAD_REQUEST)
            if len(ConsultantProfile.objects.filter(my_secretaries=recipient_request[0])) != 0:
                return Response({"error": "Target username is already secretary of you"},
                                status=status.HTTP_400_BAD_REQUEST)
            if len(SecretaryRequest.objects.filter(channel=channel[0],
                                                   target_user=recipient_request[0])) != 0:
                return Response({"error": "You already send request for this user"},
                                status=status.HTTP_400_BAD_REQUEST)
            request_serializer.validated_data['channel'] = channel[0]
            request_serializer.validated_data['target_user'] = recipient_request[0]
            secretary_request = request_serializer.save()
            return Response(data=AnswerSerializer(secretary_request).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def create_join_channel_request(self, request):
        request_serializer = JoinChannelRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            if request.user.username == request_serializer.validated_data['target_user']:
                return Response({"error": "Target username is you!!!"}, status=status.HTTP_400_BAD_REQUEST)
            channel = Channel.objects.filter(id=request_serializer.validated_data['channel'])
            if len(channel) == 0:
                return Response("Channel id is not valid", status=status.HTTP_400_BAD_REQUEST)
            if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
                    ConsultantProfile.my_secretaries.through.objects.filter(
                        consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
                return Response({"error": "You dont have permission for this request"},
                                status=status.HTTP_403_FORBIDDEN)
            recipient_request = BaseUser.objects.filter(username=request_serializer.validated_data['target_user'])
            if len(recipient_request) == 0:
                return Response({"error": "نام کاربری موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
            # if len(Channel.subscribers.through.objects.filter(user=recipient_request[0])) != 0:
            #     return Response({"error": "This username is already subscriber of this channel"},
            #                     status=status.HTTP_400_BAD_REQUEST)
            if len(JoinChannelRequest.objects.filter(channel_id=request_serializer.validated_data['channel'],
                                                     target_user=recipient_request[0])) != 0:
                return Response({"error": "شما برای این کاربر درخواست ارسال کرده اید"},
                                status=status.HTTP_400_BAD_REQUEST)
            request_serializer.validated_data['channel'] = channel[0]
            request_serializer.validated_data['target_user'] = recipient_request[0]
            join_request = request_serializer.save()
            return Response(data=AnswerSerializer(join_request).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            if request.data['request_type'] == "secretary":
                return self.create_secretary_request(request)
            elif request.data['request_type'] == "join_channel":
                return self.create_join_channel_request(request)
            else:
                return Response({"error": "request_type is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            channel = Channel.objects.filter(consultant__username=request.user.username)
            if len(channel) == 0:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            secretary_requests = SecretaryRequest.objects.filter(channel=channel[0], answer_date=None).order_by("-id")
            return Response(AnswerSerializer(secretary_requests, many=True).data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_secretary_request(self, request):
        consultant = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)
        request_id = int(request.data['request_id'])
        if len(consultant) == 0:
            return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
        secretary_request = SecretaryRequest.objects.filter(channel__consultant=consultant[0], id=request_id)
        if len(secretary_request) == 0:
            return Response("RequestId is not valid", status=status.HTTP_400_BAD_REQUEST)
        secretary_request.delete()
        return Response("request is deleted", status=status.HTTP_200_OK)

    def delete_join_channel_request(self, request):
        request_id = request.data['request_id']
        join_request = JoinChannelRequest.objects.filter(id=request_id, ).select_related(
            'channel__consultant')
        if len(join_request) == 0:
            return Response("RequestId is not valid", status=status.HTTP_400_BAD_REQUEST)
        if join_request[0].channel.consultant.baseuser_ptr_id != request.user.id and len(
                ConsultantProfile.my_secretaries.through.objects.filter(
                    consultantprofile_id=join_request[0].channel.consultant.id,
                    userprofile_id=request.user.id)) == 0:
            return Response({"error": "You dont have permission for this request"},
                            status=status.HTTP_403_FORBIDDEN)
        join_request.delete()
        return Response("request is deleted", status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        try:
            if request.data['request_type'] == "secretary":
                return self.delete_secretary_request(request)
            elif request.data['request_type'] == "join_channel":
                return self.delete_join_channel_request(request)
            else:
                return Response({"error": "Request type is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResponderRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request_id = request.data['id']
        try:
            if request.data['request_type'] == 'secretary':
                user_request = SecretaryRequest.objects.filter(id=request_id, target_user=request.user).select_related(
                    'channel')
            elif request.data['request_type'] == 'join_channel':
                user_request = JoinChannelRequest.objects.filter(id=request_id,
                                                                 target_user=request.user).select_related(
                    'channel')
            else:
                return Response({"error": "request type is not valid"}, status=status.HTTP_400_BAD_REQUEST)
            if len(user_request) == 0:
                return Response({"error": "RequestId is not valid"}, status=status.HTTP_400_BAD_REQUEST)

            answer_serializer = AnswerSerializer(user_request[0], data=request.data)
            if answer_serializer.is_valid():
                if answer_serializer.validated_data['accept'] and request.data['request_type'] == 'secretary':
                    user_request[0].channel.consultant.my_secretaries.add(request.user)
                if answer_serializer.validated_data['accept'] and request.data['request_type'] == 'join_channel':
                    user_request[0].channel.subscribers.add(request.user)
                user_request[0].delete()
                return Response(answer_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": answer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            secretary_requests = SecretaryRequest.objects.filter(target_user=request.user, answer_date=None).order_by(
                '-id')
            join_requests = JoinChannelRequest.objects.filter(target_user=request.user, answer_date=None).order_by(
                '-id')
            return Response(AnswerSerializer(list(secretary_requests) + list(join_requests), many=True).data,
                            status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class JoinChannelRequestAPI(APIView):
#     # def get(self, request, format=None):
#     #     try:
#     #         join_requests = JoinChannelRequest.objects.filter(creator=request.user)
#     #         if len(consultant) == 0:
#     #             return Response("Channel id is not valid", status=status.HTTP_400_BAD_REQUEST)
#     #         if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
#     #                 ConsultantProfile.my_secretaries.through.objects.filter(
#     #                     consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
#     #             return Response({"error": "You dont have permission for this request"},
#     #                             status=status.HTTP_403_FORBIDDEN)
#     #         join_requests = Request.objects.filter(consultant=channel[0].consultant,
#     #                                                request_type="join_channel").order_by("-id")
#     #         return Response(AnswerSerializer(join_requests, many=True).data, status=status.HTTP_200_OK)
#     #     except Exception as server_error:
#     #         return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
