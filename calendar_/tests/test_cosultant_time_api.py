from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import datetime
import pytz
from rest_framework.utils import json

from User.models import ConsultantProfile, UserProfile


class PrivateConsultantTimeTest(TestCase):
    def setUp(self):
        self.url = '/calendar/consultant-time/'
        self.client = APIClient()
        self.consultant = ConsultantProfile.objects.create(username="consultant", user_type='Immigration',
                                                           phone_number="09184576125", first_name="hossein",
                                                           last_name="masoudi", email="test1@gmailcom",
                                                           password="123456",
                                                           certificate="111")
        self.secretary = UserProfile.objects.create(username="secretary", email="reza@gmail.com", password="123456",
                                                    phone_number="09176273745", first_name="reza", last_name="rezaee")

        self.consultant.my_secretaries.add(self.secretary)
        self.normal_user = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")

    def test_un_authorize_client_post_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_post_request(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            'consultant_id': 1
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_secretary_post_request_successfully(self):
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 19, 30)).__str__()
        payload = {
            "id": 1,
            "title": "consultant_time",
            "description": "consultant_time",
            "consultant_id": 1,
            "start_date": start_date,
            'end_date': end_date
        }

        self.client.force_authenticate(self.secretary)
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content), payload)

    def test_invalid_consultant_id_secretary_post_request(self):
        self.client.force_authenticate(self.secretary)
        payload = {
            'consultant_id': 10
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_consultant_post_request_successfully(self):
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 19, 30)).__str__()
        payload = {
            "id": 1,
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }

        self.client.force_authenticate(self.consultant)
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content), payload)

    def test_invalid_start_date(self):
        self.client.force_authenticate(self.consultant)
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2002, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 19, 30)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_end_date(self):
        self.client.force_authenticate(self.consultant)
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
