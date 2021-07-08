import os

from django.core.files.base import File
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json
from channel.models import Channel
from User.models import *


class PrivateUserProfileTest(TestCase):
    def setUp(self):
        self.url = "/profile/"
        self.client = APIClient()
        # base_address = os.path.dirname(__file__)
        # certificate = open(base_address + '/certificate/consultant.pdf', 'rb')
        self.consultant = ConsultantProfile.objects.create(username="consultant", user_type='Immigration',
                                                           phone_number="09184576125", first_name="hossein",
                                                           last_name="masoudi", email="test1@gmail.com",
                                                           password="123456", avatar="File(avatar)",
                                                           certificate="File(certificate)")
        # certificate.close()
        self.user = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                               password="123456",
                                               phone_number="09176273746", first_name="hamid",
                                               last_name="azarbad", avatar="File(avatar)", )

        self.consultant_channel = Channel.objects.create(name="rasoul", description="immegrate to Germany",
                                                         invite_link='Immigrate-Germany',
                                                         consultant=self.consultant)

    def test_un_authorize_client(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_normal_user_profile(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'id': 2, 'username': self.user.username,
                          'avatar': 'https://res.cloudinary.com/iust/image/upload/File%28avatar%29',
                          'email': self.user.email,
                          'first_name': self.user.first_name, 'last_name': self.user.last_name,
                          'phone_number': self.user.phone_number, 'private_profile': False, 'user_type': 'normal_user'},
                         json.loads(response.content))

    def test_get_consultant_profile(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'id': 1, 'username': self.consultant.username,
                          'avatar': 'https://res.cloudinary.com/iust/image/upload/File%28avatar%29',
                          'email': self.consultant.email,
                          'first_name': self.consultant.first_name, 'last_name': self.consultant.last_name,
                          'phone_number': self.consultant.phone_number, 'private_profile': False,
                          'user_type': 'Immigration',
                          'certificate': 'https://res.cloudinary.com/iust/image/upload/File%28certificate%29'},
                         json.loads(response.content))

    def test_put_normal_user_profile(self):
        self.client.force_authenticate(self.user)
        payload = {
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'password': self.user.password,
            'phone_number': "09123988601",
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_user = UserProfile.objects.filter(username='normal_user')[0]
        self.assertEqual(new_user.phone_number, "09123988601")

    def test_put_normal_user_repetitious_username(self):
        self.client.force_authenticate(self.consultant)
        payload = {
            'username': self.user.username,
            'email': self.consultant.email,
            'first_name': self.consultant.first_name,
            'last_name': self.consultant.last_name,
            'password': self.consultant.password,
            'phone_number': self.consultant.phone_number,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "نام‌کاربری تکراری است"})

    def test_put_normal_user_repetitious_email(self):
        self.client.force_authenticate(self.consultant)
        payload = {
            'username': self.consultant.username,
            'email': self.user.email,
            'first_name': self.consultant.first_name,
            'last_name': self.consultant.last_name,
            'password': self.consultant.password,
            'phone_number': self.consultant.phone_number,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "ایمیل تکراری است"})

    def test_put_normal_user_repetitious_phone_number(self):
        self.client.force_authenticate(self.consultant)
        payload = {
            'username': self.consultant.username,
            'email': self.consultant.email,
            'first_name': self.consultant.first_name,
            'last_name': self.consultant.last_name,
            'password': self.consultant.password,
            'phone_number': self.user.phone_number,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شماره‌تلفن تکراری است"})

    def test_get_another_profile_invalid_username(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "consultant1/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({'error': "کاربری با این نام‌کاربری موجود نیست"},
                         json.loads(response.content))

    def test_get_another_profile(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + self.consultant.username + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'id': 1, 'username': self.consultant.username,
                          'avatar': 'https://res.cloudinary.com/iust/image/upload/File%28avatar%29',
                          'first_name': self.consultant.first_name, 'last_name': self.consultant.last_name,
                          'private_profile': False, 'user_type': 'Immigration',
                          'certificate': 'https://res.cloudinary.com/iust/image/upload/File%28certificate%29',
                          "channel_id": self.consultant_channel.id},
                         json.loads(response.content))
