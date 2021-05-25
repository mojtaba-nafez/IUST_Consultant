from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from User.models import ConsultantProfile, UserProfile, BaseUser
from message.models import DirectMessage

class ConnectedUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user_id = request.user.id
            from django.db.models import Q
            
            # receiver = DirectMessage.objects.filter(Q(sender__id=user_id) | Q(reciever__id=user_id)).order_by().values_list('reciever').distinct()

            sender = DirectMessage.objects.filter(Q(reciever__id=user_id)).order_by().values_list('sender').distinct()
            receiver = DirectMessage.objects.filter(Q(sender__id=user_id)).order_by().values_list('reciever').distinct()
            connected_users_query_set = sender.union(receiver)
            connected_users_list = []
            for user_id in connected_users_query_set:
                user = BaseUser.objects.get(id=user_id[0])
                connected_users_list.append(
                    {
                        "id" : user.id,
                        "username":user.username,
                        "first_name": user.first_name,
                        "last_name":user.last_name,
                        "user_type": user.user_type,
                        "email":user.email,
                        "phone_number":user.phone_number,
                        "avatar" : user.avatar.url if user.avatar else None
                    }
                )
 
            return Response(connected_users_list, status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
