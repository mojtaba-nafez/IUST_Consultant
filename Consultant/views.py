from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from channel.models import Channel, Subscription
from User.models import ConsultantProfile, UserProfile
from message.models import *

class InsertFakeData(APIView):
    def get(self, request, format=None):
        try: 
            
            #consultant=ConsultantProfile.objects.create(username="testttttt",user_type='Immigration', phone_number="09185676125", first_name="hosseiniiiiii", last_name="masoudiiiiiii", email="testtttttt@gmailcom",password='fdfddfxcsd', certificate="111")
            #channel=Channel.objects.create(name="chchchchc",description= "immegrate to Germany-------", invite_link='Immigrate-Germany-------------', consultant=consultant)            
            #user = UserProfile.objects.create(username="ffffffffffff", email="ffffffffff@gmail.com", password="ffffffff", phone_number="09178125538",first_name="fffffff", last_name="fffff")
            #Subscription.objects.create(channel=channel, user=user)
            #print('user '+ user.username+' subscribe to channel '+ channel.name )

            
            ##   Normal User info:
            user_user_name = ['mostafa', 'ali', 'saeed'] # 'ahamd', 'rahim', 'abass'
            user_email = ['mojtaba@gmail.com', 'ali@gmail.com', 'saeed@gmail.com']
            user_phone_number = ['09189152654', '09136785425', '09163258714']
            user_first_name = ['mojtaba', 'ali', 'saeed']
            user_last_name = ['nafez', 'hosseini', 'ebrahimi']
            user_password =['qwe12222', '43fte32e', 'sdfakjl23']


            # Consultant Info + his channel
            consultant_type = ['Lawyer', 'medical', 'EntranceExam'] #  'Psychology', 'Immigration', 'AcademicAdvice'
            consultant_username = ['Hossein', 'Hamid', "Behrouz"]
            consultant_phone_number = ['09168745698', '09123256548', '09187485698']
            consultant_email = ['Hossein@gmail.com', 'Hamid@gmail.com', 'Behrouz@gmail.com']
            consultant_first_name = ['hosseini_MJ', 'hammidiali', 'behrouz__Fg']
            consultant_last_name = ['hosseini', 'hammidi', 'behbahani']
            consultant_password =['fdsajklsd', '34fgtjrvmk', 'fkjvnueir']
            invite_link = ['wint-the-court', 'be-care-full', 'become-the-best-of-you']
            description = ['hire me. win the right', 'we will optimze your family', 'be in the first palce of Entrance Exam']
            channel_name = ['BestLayers', 'DoctorSalam', 'Parvaz']
            
            message_text = ["welcome.", 'injoy the channel content.', 'glad to meet you']
            users = []
            for i in range(len(user_user_name)):
                try:
                    user = UserProfile.objects.create(username=user_user_name[i], email=user_email[i], password=user_password[i], phone_number=user_phone_number[i],first_name=user_first_name[i], last_name=user_last_name[i])
                    users.append(user)
                    print('user '+user_user_name[i]+ ' created')
                except:
                    pass

            consultants = []
            channels=[]
            for j in range(len(consultant_username)):
                try:
                    consultant=ConsultantProfile.objects.create(username=consultant_username[j],user_type=consultant_type[j], phone_number=consultant_phone_number[j], first_name=consultant_first_name[j], last_name=consultant_last_name[j], email=consultant_email[j], password=consultant_password[j], certificate="111")
                    consultants.append(consultant)
                    print('consultant '+ consultant_username[j]+' created')
                    channel=Channel.objects.create(name=channel_name[j],description= description[j], invite_link=invite_link[j], consultant=consultant)        
                    print('channel '+ channel_name[j]+' created')
                    channels.append(channel)
                    for k in range(len(message_text)):
                        try:
                            print("i wat to add : " + message_text[k])
                            ChannelMessage.objects.create(text=message_text[k], message_type='text', channel=channel, creator=consultant)
                            print('message '+ message_text[k]+' added to channel'+ channel.name)
                        except:
                            print("can not add : " + message_text[k]+ ' to channel ',  channel.name + ' consultant: '+consultant.username)
                    for i in range(len(users)):
                        try:
                            Subscription.objects.create(channel=channel, user=users[i])
                            print('user '+ users[i].username+' subscribe to channel '+ channel.name )
                        except:
                            print("try")
                except:
                    pass
            return Response(data={ "status": "ok"}, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

