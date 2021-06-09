from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.base import File
import os

from rest_framework.utils import json

from channel.models import Channel
from User.models import ConsultantProfile, UserProfile
from message.models import ChannelMessage


class PrivateChannelMessageApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/channel-message/"
        self.consultant = ConsultantProfile.objects.create(username="test", phone_number="09184576125",
                                                           first_name="hossein", last_name="masoudi",
                                                           email="test1@gmailcom", password="123456",
                                                           certificate="111", user_type='Lawyer')
        self.channel = Channel.objects.create(name="test", description="test", invite_link='test',
                                              consultant=self.consultant)
        self.secretary = UserProfile.objects.create(username="secretary", email="reza@gmail.com", password="123456",
                                                    phone_number="09176273745", first_name="reza", last_name="rezaee")

        self.consultant.my_secretaries.add(self.secretary)
        self.normal_user = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")

        self.message_types = ['t', 'i', 'v', 'a']
        # self.audio_file = None
        # self.video_file = None
        base_address = os.path.dirname(__file__)
        self.message_files_address = [None, base_address + "/files/test.png", base_address + "/files/test.mp3",
                                      base_address + "/files/test.mp4"]
        self.channel_messages = []
        for i in range(20):
            message_file = None
            if i % 4 == 1:
                message_file = open(self.message_files_address[i % 4], 'rb')
            new_message = ChannelMessage.objects.create(text="new message",
                                                        message_file=File(message_file),
                                                        message_type=self.message_types[i % 4], channel=self.channel,
                                                        creator=self.consultant)
            self.channel_messages += [new_message]
            if message_file is not None:
                message_file.close()

    def test_un_authorize_client(self):
        response = self.client.put(self.url + "1/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(self.url + "1/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_channel_message_invalid_channel_id(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url + '3/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه کانال موجود نیست"})

    def test_get_channel_message(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url + '1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)['results']), 10)
        self.assertEqual(json.loads(response.content)['count'], 20)
        self.assertEqual(json.loads(response.content)['next'], 'http://testserver/channel-message/1/?page=2')

    def test_post_channel_message_invalid_channel_id(self):
        self.client.force_authenticate(self.secretary)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'text': "salam",
            "message_type": "t",
            "message_file": file
        }
        response = self.client.post(self.url + "10/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه کانال موجود نیست"})

    def test_post_channel_message_forbidden(self):
        self.client.force_authenticate(self.normal_user)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'id': 21,
            'text': "salam",
            "message_type": "i",
            "message_file": file
        }
        response = self.client.post(self.url + "1/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما مجوز انجام این کار را ندارید"})

    def test_post_channel_message_consultant_successfully(self):
        self.client.force_authenticate(self.consultant)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'text': "salam",
            "message_type": "i",
            "message_file": file
        }
        response = self.client.post(self.url + "1/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_channel_message_secretary_successfully(self):
        self.client.force_authenticate(self.secretary)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'text': "salam",
            "message_type": "i",
            "message_file": file
        }
        response = self.client.post(self.url + "1/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_channel_message_invalid_message_id(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "1/100/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی پیام صحیح نیست"})

    def test_delete_channel_message_invalid_channel_id(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "100/1/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی کانال صحیح نیست"})

    def test_delete_channel_message_noncompliance_channel_message_id(self):
        another_consultant = ConsultantProfile.objects.create(username="test2", phone_number="09184576129",
                                                              first_name="hossein", last_name="masoudi",
                                                              email="test12@gmailcom", password="123456",
                                                              certificate="111", user_type='Lawyer')
        another_channel = Channel.objects.create(name="test", description="test", invite_link='test2',
                                                 consultant=another_consultant)
        self.client.force_authenticate(another_consultant)
        response = self.client.delete(self.url + "2/1/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی کانال و پیام با هم مطابقت ندارد"})

    def test_delete_channel_message_forbidden(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.delete(self.url + "1/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما مجوز چنین کاری را ندارید"})

    def test_delete_channel_message_consultant_successfully(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "1/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), "پیام حذف شد")

    def test_delete_channel_message_secretary_successfully(self):
        self.client.force_authenticate(self.secretary)
        response = self.client.delete(self.url + "1/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), "پیام حذف شد")

    def test_put_channel_message_invalid_message_id(self):
        self.client.force_authenticate(self.consultant)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'text': "salam",
            "message_type": "i",
            "message_file": file
        }
        response = self.client.put(self.url + "1/100/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی پیام صحیح نیست"})

    def test_put_channel_message_invalid_channel_id(self):
        self.client.force_authenticate(self.consultant)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'text': "salam",
            "message_type": "i",
            "message_file": file
        }
        response = self.client.put(self.url + "100/1/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی کانال صحیح نیست"})

    def test_put_channel_message_noncompliance_channel_message_id(self):
        another_consultant = ConsultantProfile.objects.create(username="test2", phone_number="09184576129",
                                                              first_name="hossein", last_name="masoudi",
                                                              email="test12@gmailcom", password="123456",
                                                              certificate="111", user_type='Lawyer')
        another_channel = Channel.objects.create(name="test", description="test", invite_link='test2',
                                                 consultant=another_consultant)
        self.client.force_authenticate(another_consultant)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'text': "salam",
            "message_type": "i",
            "message_file": file
        }
        response = self.client.put(self.url + "2/1/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی کانال و پیام با هم مطابقت ندارد"})

    def test_put_channel_message_forbidden(self):
        self.client.force_authenticate(self.normal_user)
        file = File(open(self.message_files_address[1], 'rb'))
        payload = {
            'text': "salam",
            "message_type": "i",
            "message_file": file
        }
        response = self.client.put(self.url + "1/1/", payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما مجوز چنین کاری را ندارید"})

    def test_put_channel_message_consultant_successfully(self):
        self.client.force_authenticate(self.consultant)
        payload = {
            'text': "salam",
            "message_type": "i",
        }
        response = self.client.put(self.url + "1/1/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_message = ChannelMessage.objects.filter(id=1)[0]
        self.assertEqual(new_message.text, "salam")

    def test_put_channel_message_secretary_successfully(self):
        self.client.force_authenticate(self.secretary)
        payload = {
            'text': "salam",
            "message_type": "i",
        }
        response = self.client.put(self.url + "1/1/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_message = ChannelMessage.objects.filter(id=1)[0]
        self.assertEqual(new_message.text, "salam")
