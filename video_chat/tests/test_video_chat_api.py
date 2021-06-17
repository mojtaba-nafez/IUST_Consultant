import datetime

from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.utils import timezone
from rest_framework.utils import json

from User.models import ConsultantProfile, UserProfile
from calendar_.models import ConsultantTime


class PrivateVideoChatTest(TestCase):
    def setUp(self):
        self.url = '/video-chat/consultant-time/start/'
        self.client = APIClient()
        self.consultant = ConsultantProfile.objects.create(username="consultant", user_type='Immigration',
                                                           phone_number="09184576125", first_name="hossein",
                                                           last_name="masoudi", email="test1@gmailcom",
                                                           password="123456",
                                                           certificate="111")
        self.reservatore = UserProfile.objects.create(username="reservatore", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")
        self.un_reservatore = UserProfile.objects.create(username="normal_user", email="hamid2@gmail.com",
                                                         password="123456",
                                                         phone_number="09176273747", first_name="hamid",
                                                         last_name="azarbad")
        self.reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=self.reservatore,
                                                                      title="title", description="description",
                                                                      start_date=timezone.now(),
                                                                      end_date=timezone.now() + datetime.timedelta(
                                                                          hours=1))
        self.un_reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=None,
                                                                         title="title", description="description",
                                                                         start_date=timezone.now() + datetime.timedelta(
                                                                             hours=3),
                                                                         end_date=timezone.now() + datetime.timedelta(
                                                                             hours=4))
        self.old_reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant,
                                                                          user=self.reservatore,
                                                                          title="title", description="description",
                                                                          start_date=timezone.now() - datetime.timedelta(
                                                                              hours=3),
                                                                          end_date=timezone.now() - datetime.timedelta(
                                                                              hours=2))
        self.future_reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant,
                                                                             user=self.reservatore,
                                                                             title="title", description="description",
                                                                             start_date=timezone.now() + datetime.timedelta(
                                                                                 hours=1),
                                                                             end_date=timezone.now() + datetime.timedelta(
                                                                                 hours=2))

    def test_un_authorize_client(self):
        response = self.client.post(self.url + "100/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_consultant_time_id_in_start_video_chat(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.post(self.url + "1000/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی زمان‌مشاوره صحیح نیست"})

    # def test_start_request_for_un_reserved_consultant_time(self):
    #     self.client.force_authenticate(self.consultant)
    #     response = self.client.post(self.url + self.un_reserved_consultant_time.id.__str__() + "/")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(json.loads(response.content), {"error": "این زمان رزرو نشده است"})

    # def test_un_reservatore_user_request_for_video_chat(self):
    #     self.client.force_authenticate(self.un_reservatore)
    #     response = self.client.post(self.url + self.reserved_consultant_time.id.__str__() + "/")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(json.loads(response.content), {"error": "دسترسی به این زمان‌مشاوره را ندارید"})

    def test_start_request_for_old_reserved_consultant_time(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.post(self.url + self.old_reserved_consultant_time.id.__str__() + "/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "زمان مشاوره به‌اتمام رسیده‌است"})

    def test_start_request_for_future_reserved_consultant_time(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.post(self.url + self.future_reserved_consultant_time.id.__str__() + "/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "زمان مشاوره فرانرسیده‌است"})

    def test_start_request_for_reserved_consultant_time(self):
        self.client.force_authenticate(self.consultant)
        consultant_response = self.client.post(self.url + self.reserved_consultant_time.id.__str__() + "/")
        self.assertEqual(consultant_response.status_code, status.HTTP_200_OK)
        consultant_request_response_data = json.loads(consultant_response.content)
        self.assertIsNotNone(consultant_request_response_data['meetingId'])
        self.assertIsNotNone(consultant_request_response_data['hostRoomUrl'])

        self.client.force_authenticate(self.reservatore)
        reservatore_response = self.client.post(self.url + self.reserved_consultant_time.id.__str__() + "/")
        self.assertEqual(reservatore_response.status_code, status.HTTP_200_OK)
        reservatore_request_response_data = json.loads(reservatore_response.content)
        self.assertEqual(reservatore_request_response_data['meetingId'], consultant_request_response_data['meetingId'])
        self.assertIsNone(reservatore_request_response_data['hostRoomUrl'])
