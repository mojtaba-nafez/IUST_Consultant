from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json

from User.models import ConsultantProfile, UserProfile


class PublicSignUpTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_login_url = "/user/login/"
        self.user_logout_url = "/user/logout/"
        self.consultant_login_url = "/consultant/login/"
        self.consultant = ConsultantProfile.objects.create(username="consultant", phone_number="09184576125",
                                                           first_name="hossein", last_name="masoudi",
                                                           email="test1@gmail.com", password="123456",
                                                           certificate="111", user_type='Lawyer')
        self.normal_user = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")

    def test_sign_up_invalid_username_and_email(self):
        payload = {
            "email_username": "test",
            "password": "123456"
        }
        response = self.client.post(self.user_login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "کاربری با این مشخصات وجود ندارد"})

    def test_sign_up_invalid_password(self):
        payload = {
            "email_username": "consultant",
            "password": "1234567"
        }
        response = self.client.post(self.user_login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "رمز‌عبور صحیح نیست"})

    def test_sign_up_successfully(self):
        payload = {
            "email_username": "consultant",
            "password": "123456"
        }
        response = self.client.post(self.user_login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_un_authorize_logout(self):
        response = self.client.post(self.user_logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_logout_successfully(self):
    #     self.client.force_authenticate(self.consultant)
    #     response = self.client.post(self.user_logout_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)