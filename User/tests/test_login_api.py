from django.test import TestCase
from rest_framework.test import APIClient


class PublicSignUpTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_signup_url = "user/login/"
        self.consultant_signup_url = "consultant/login/"

    def test_sign_up_invalid_phone_number(self):
        payload = {

        }
        response = self.client.post(self.user_signup_url, payload)