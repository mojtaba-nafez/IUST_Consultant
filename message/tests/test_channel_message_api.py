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
        payload = {
            'id': 21,
            'text': "salam",
            "message_type": "t",
            "message_file": None
        }
        response = self.client.post(self.url + "10/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه کانال موجود نیست"})