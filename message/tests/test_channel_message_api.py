from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.base import File
import os
from channel.models import Channel
from User.models import ConsultantProfile
from message.models import ChannelMessage


class PrivateChannelMessageApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.consultant = ConsultantProfile.objects.create(username="test", phone_number="09184576125",
                                                           first_name="hossein", last_name="masoudi",
                                                           email="test1@gmailcom", password="123456",
                                                           certificate="111", user_type='Lawyer')
        self.client.force_authenticate(self.consultant)
        self.channel = Channel.objects.create(name="test", description="test", invite_link='test',
                                              consultant=self.consultant)
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

    def test_get_channel_message(self):
        response = self.client.get('/channel-message/1/?page=1')
        print(response)
