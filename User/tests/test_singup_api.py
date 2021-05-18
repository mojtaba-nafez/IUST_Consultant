import os

from django.core.files import File
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json

from User.models import ConsultantProfile, UserProfile


class PublicSignUpTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_signup_url = "/user/signup/"
        self.consultant_signup_url = "/consultant/signup/"
        self.consultant = ConsultantProfile.objects.create(username="consultant", phone_number="09184576125",
                                                           first_name="hossein", last_name="masoudi",
                                                           email="test1@gmail.com", password="123456",
                                                           certificate="111", user_type='Lawyer')
        self.normal_user = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")

    def test_sign_up_invalid_phone_number(self):
        payload = {
            "username": "hamidreza",
            "email": "hamidreza@gmail.com",
            "first_name": "hamidreza",
            "last_name": "azarbad",
            "phone_number": "0912398860",
            "password": "123456"
        }
        response = self.client.post(self.user_signup_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'error': {'phone_number': ['فرمت شماره‌تلفن صحیح نیست']}})

    def test_sign_up_repetitious_username(self):
        payload = {
            "username": "consultant",
            "email": "hamidreza@gmail.com",
            "first_name": "hamidreza",
            "last_name": "azarbad",
            "phone_number": "09123988601",
            "password": "123456"
        }
        response = self.client.post(self.user_signup_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "نام‌کاربری تکراری است"})

    def test_sign_up_repetitious_email(self):
        payload = {
            "username": "hamidreza",
            "email": "test1@gmail.com",
            "first_name": "hamidreza",
            "last_name": "azarbad",
            "phone_number": "09123988601",
            "password": "123456"
        }
        response = self.client.post(self.user_signup_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "ایمیل تکراری است"})

    def test_sign_up_repetitious_phone_number(self):
        payload = {
            "username": "hamidreza",
            "email": "hamidreza@gmail.com",
            "first_name": "hamidreza",
            "last_name": "azarbad",
            "phone_number": "09184576125",
            "password": "123456"
        }
        response = self.client.post(self.user_signup_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شماره‌تلفن تکراری است"})

    def test_sign_up_normal_user_successfully(self):
        payload = {
            "username": "hamidreza",
            "email": "hamidreza@gmail.com",
            "first_name": "hamidreza",
            "last_name": "azarbad",
            "phone_number": "09123988601",
            "password": "123456"
        }
        response = self.client.post(self.user_signup_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_user = UserProfile.objects.filter(username='hamidreza')
        self.assertEqual(len(new_user), 1)

    def test_sign_up_consultant_successfully(self):
        file = File(open(os.path.dirname(__file__) + "/certificate/consultant.pdf", 'rb'))
        payload = {
            "username": "hamidreza",
            "email": "hamidreza@gmail.com",
            "first_name": "hamidreza",
            "last_name": "azarbad",
            "phone_number": "09123988601",
            "password": "123456",
            "certificate": file,
            'user_type': "Lawyer",
        }
        response = self.client.post(self.consultant_signup_url, payload)
        file.close()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_user = ConsultantProfile.objects.filter(username='hamidreza')
        self.assertEqual(len(new_user), 1)