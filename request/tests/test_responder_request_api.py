from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json

from User.models import *
from channel.models import Channel
from request.models import JoinChannelRequest


class PrivateResponderRequestAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/request/responder/"
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

        self.join_channel_request = JoinChannelRequest.objects.create(target_user=self.normal_user,
                                                                      request_type="join_channel",
                                                                      request_text="join to my channel",
                                                                      channel=self.channel, request_date="2021-05-21T06:24:47.208955Z")

    def test_un_authorize_client(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_request_successfully(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [
            {'id': 1, 'channel': {'id': 1, 'name': 'test', 'invite_link': 'test'},
             'target_user': {'username': 'normal_user', 'email': 'hamid@gmail.com'},
             'request_text': 'join to my channel', 'answer_text': None, 'request_date': '2021-05-21T06:24:47.208955Z',
             'answer_date': None, 'accept': False, 'request_type': 'join_channel'}
        ])

    # def test_post_request_join_channel_invalid_request_id(self):
    #     self.client.force_authenticate(self.normal_user)
    #     payload = {
    #         "id": 1
    #         "channel"
    #     }
    #     response = self.client.post(self.url ,  payload)
