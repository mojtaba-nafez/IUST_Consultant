from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import datetime
import pytz
from django.utils import timezone as tz
from rest_framework.utils import json

from User.models import ConsultantProfile, UserProfile
from calendar_.models import ConsultantTime


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
        timezone = pytz.timezone('UTC')
        self.un_reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=None,
                                                                         title="title", description="description",
                                                                         start_date=timezone.localize(
                                                                             datetime.datetime(2026, 1, 1, 18,
                                                                                               30)).__str__(),
                                                                         end_date=timezone.localize(
                                                                             datetime.datetime(2026, 1, 1, 19,
                                                                                               30)).__str__())
        self.reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=self.normal_user,
                                                                      title="title", description="description",
                                                                      start_date=timezone.localize(
                                                                          datetime.datetime(2027, 1, 1, 18,
                                                                                            30)).__str__(),
                                                                      end_date=timezone.localize(
                                                                          datetime.datetime(2027, 1, 1, 19,
                                                                                            30)).__str__())
        self.consultant2 = ConsultantProfile.objects.create(username="consultant2", user_type='Immigration',
                                                            phone_number="09184576128", first_name="hossein",
                                                            last_name="masoudi", email="test12@gmailcom",
                                                            password="123456",
                                                            certificate="111")
        self.consultant2.my_secretaries.add(self.secretary)
        self.un_reserved_consultant_time2 = ConsultantTime.objects.create(consultant=self.consultant2, user=None,
                                                                          title="title", description="description",
                                                                          start_date=timezone.localize(
                                                                              datetime.datetime(2027, 1, 1, 18,
                                                                                                30)).__str__(),
                                                                          end_date=timezone.localize(
                                                                              datetime.datetime(2027, 1, 1, 19,
                                                                                                30)).__str__())
        self.un_reserved_consultant_time3 = ConsultantTime.objects.create(consultant=self.consultant, user=None,
                                                                          title="title", description="description",
                                                                          start_date=timezone.localize(
                                                                              datetime.datetime(2026, 1, 1, 18,
                                                                                                30)).__str__(),
                                                                          end_date=timezone.localize(
                                                                              datetime.datetime(2026, 1, 1, 19,
                                                                                                30)).__str__())

    def test_un_authorize_client(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_consultant_times_without_date_query_param(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "تاریخ را نفرستاده اید"})

    def test_get_consultant_times_wrong_date_format(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url + "?date=545488")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "فرمت تاریخ درست نیست"})

    def test_normal_user_get_consultant_times(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.url + "?date=2027-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [
            {
                "id": 2,
                "start_date": "2027-01-01T18:30:00Z",
                "end_date": '2027-01-01T19:30:00Z',
                "title": "title",
                "description": "description",
                "user": {
                    "id": 3,
                    "username": self.normal_user.username,
                    "first_name": self.normal_user.first_name,
                    "last_name": self.normal_user.last_name,
                    "phone_number": self.normal_user.phone_number,
                    "avatar": self.normal_user.avatar,
                },
                "consultant": {
                    "id": 1,
                    "username": "consultant",
                    "phone_number": "09184576125",
                    "avatar": None
                },
            }
        ])

    def test_consultant_get_consultant_times(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url + "?date=2027-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [
            {
                "id": 2,
                "start_date": "2027-01-01T18:30:00Z",
                "end_date": '2027-01-01T19:30:00Z',
                "title": "title",
                "description": "description",
                "user": {
                    "id": 3,
                    "username": self.normal_user.username,
                    "first_name": self.normal_user.first_name,
                    "last_name": self.normal_user.last_name,
                    "phone_number": self.normal_user.phone_number,
                    "avatar": self.normal_user.avatar,
                },
                "consultant": {
                    "id": 1,
                    "username": "consultant",
                    "phone_number": "09184576125",
                    "avatar": None
                },
            }
        ])

    def test_secretary_get_consultant_times(self):
        self.client.force_authenticate(self.secretary)
        response = self.client.get(self.url + "?date=2027-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [
            {
                "id": 2,
                "start_date": "2027-01-01T18:30:00Z",
                "end_date": '2027-01-01T19:30:00Z',
                "title": "title",
                "description": "description",
                "user": {
                    "id": 3,
                    "username": self.normal_user.username,
                    "first_name": self.normal_user.first_name,
                    "last_name": self.normal_user.last_name,
                    "phone_number": self.normal_user.phone_number,
                    "avatar": self.normal_user.avatar,
                },
                "consultant": {
                    "id": 1,
                    "username": "consultant",
                    "phone_number": "09184576125",
                    "avatar": None
                },
            },
            {
                "id": 3,
                "start_date": "2027-01-01T18:30:00Z",
                "end_date": '2027-01-01T19:30:00Z',
                "title": "title",
                "description": "description",
                "user": None,
                "consultant": {
                    "id": 4,
                    "username": "consultant2",
                    "phone_number": "09184576128",
                    "avatar": None
                },
            }
        ])

    def test_normal_user_post_request(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            'consultant_id': 1
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما منشی این مشاور نیستید"})

    def test_secretary_post_request_successfully(self):
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 19, 30)).__str__()
        payload = {
            "id": 1,
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
        self.assertEqual(json.loads(response.content), {"error": "مشاوری با این شناسه موجود نیست"})

    def test_consultant_post_request_successfully(self):
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 19, 30)).__str__()
        payload = {
            "id": 1,
            "start_date": start_date,
            'end_date': end_date
        }

        self.client.force_authenticate(self.consultant)
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content), payload)

    def test_invalid_start_date_post_request(self):
        self.client.force_authenticate(self.consultant)
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2002, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 19, 30)).__str__()
        payload = {
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {"error": {"start_date": ['زمان شروع، از زمان حال قدیمی تر است']}})

    def test_invalid_end_date_post_request(self):
        self.client.force_authenticate(self.consultant)
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        end_date = timezone.localize(datetime.datetime(2022, 1, 1, 18, 30)).__str__()
        payload = {
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': {'non_field_errors': ['زمان پایان از زمان شروع قدیمی تر است']}})

    def test_interference_consultant_time_post_request(self):
        self.client.force_authenticate(self.consultant)
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2026, 1, 1, 19, 00)).__str__()
        end_date = timezone.localize(datetime.datetime(2026, 1, 1, 19, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.un_reserved_consultant_time.id})
        start_date = timezone.localize(datetime.datetime(2026, 1, 1, 15, 00)).__str__()
        end_date = timezone.localize(datetime.datetime(2026, 1, 1, 18, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.un_reserved_consultant_time.id})
        start_date = timezone.localize(datetime.datetime(2026, 1, 1, 18, 15)).__str__()
        end_date = timezone.localize(datetime.datetime(2026, 1, 1, 18, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.un_reserved_consultant_time.id})
        start_date = timezone.localize(datetime.datetime(2026, 1, 1, 18, 45)).__str__()
        end_date = timezone.localize(datetime.datetime(2026, 1, 1, 19, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.un_reserved_consultant_time.id})

    def test_normal_user_put_request(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.put(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این کار را ندارید"})

    def test_invalid_consultant_time_id_put_request(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.put(self.url + "10/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه زمان مشاوره موجود نیست"})

    def test_put_request_un_reserved_consultant_time_successfully(self):
        timezone = pytz.timezone('UTC')
        update_start_date = timezone.localize(datetime.datetime(2023, 1, 1, 18, 30)).__str__()
        update_end_date = timezone.localize(datetime.datetime(2023, 1, 1, 19, 30)).__str__()
        payload = {
            "id": 1,
            "start_date": update_start_date,
            "end_date": update_end_date,
        }
        self.client.force_authenticate(self.consultant)
        response = self.client.put(self.url + "1/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_consultant_time = ConsultantTime.objects.filter(id=1)[0]
        self.assertEqual({
            "id": update_consultant_time.id,
            "start_date": update_consultant_time.start_date.__str__(),
            "end_date": update_consultant_time.end_date.__str__(),
        }, payload)
        self.client.force_authenticate(self.secretary)
        response = self.client.put(self.url + "1/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_request_reserved_consultant_time_successfully(self):
        timezone = pytz.timezone('UTC')
        update_start_date = timezone.localize(datetime.datetime(2024, 1, 1, 18, 30)).__str__()
        update_end_date = timezone.localize(datetime.datetime(2024, 1, 1, 19, 30)).__str__()
        payload = {
            "id": 2,
            "start_date": update_start_date,
            "end_date": update_end_date,
        }
        self.client.force_authenticate(self.consultant)
        response = self.client.put(self.url + "2/", payload)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(json.loads(response.content)['message'], "باید منتظر تایید کاربر رزروکننده بمانید")
        self.client.force_authenticate(self.secretary)
        response = self.client.put(self.url + "2/", payload)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_interference_consultant_time_put_request(self):
        self.client.force_authenticate(self.consultant)
        timezone = pytz.timezone('UTC')
        start_date = timezone.localize(datetime.datetime(2027, 1, 1, 19, 00)).__str__()
        end_date = timezone.localize(datetime.datetime(2027, 1, 1, 19, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.put(self.url + "4/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.reserved_consultant_time.id})
        start_date = timezone.localize(datetime.datetime(2027, 1, 1, 15, 00)).__str__()
        end_date = timezone.localize(datetime.datetime(2027, 1, 1, 18, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.put(self.url + "4/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.reserved_consultant_time.id})
        start_date = timezone.localize(datetime.datetime(2027, 1, 1, 18, 15)).__str__()
        end_date = timezone.localize(datetime.datetime(2027, 1, 1, 18, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.put(self.url + "4/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.reserved_consultant_time.id})
        start_date = timezone.localize(datetime.datetime(2027, 1, 1, 18, 45)).__str__()
        end_date = timezone.localize(datetime.datetime(2027, 1, 1, 19, 45)).__str__()
        payload = {
            "title": "consultant_time",
            "description": "consultant_time",
            "start_date": start_date,
            'end_date': end_date
        }
        response = self.client.put(self.url + "4/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {'error': "با ساعت‌مشاوره‌ی دیگری تداخل دارد",
                          "consultant_time_id": self.reserved_consultant_time.id})

    def test_invalid_consultant_time_id_delete_request(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "10/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه زمان مشاوره موجود نیست"})

    def test_normal_user_delete_request(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این کار را ندارید"})

    def test_un_reserved_consultant_time_delete_request(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(ConsultantTime.objects.filter(id=1)), 0)

    def test_reserved_consultant_time_delete_request(self):
        self.client.force_authenticate(self.secretary)
        response = self.client.delete(self.url + "2/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(ConsultantTime.objects.filter(id=2)), 1)
        self.assertEqual(json.loads(response.content),
                         {"error": "این ساعت را کاربری رزرو کرده است. در صورت نیاز باید آن را لغو کنید."})


class PrivateCancelConsultantTimeTest(TestCase):
    def setUp(self):
        self.url = '/calendar/consultant-time/cancel/'
        self.client = APIClient()
        self.consultant = ConsultantProfile.objects.create(username="consultant", user_type='Immigration',
                                                           phone_number="09184576125", first_name="hossein",
                                                           last_name="masoudi", email="test1@gmailcom",
                                                           password="123456",
                                                           certificate="111")
        self.secretary = UserProfile.objects.create(username="secretary", email="reza@gmail.com", password="123456",
                                                    phone_number="09176273745", first_name="reza", last_name="rezaee")

        self.consultant.my_secretaries.add(self.secretary)
        self.reservatore = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")
        timezone = pytz.timezone('UTC')
        self.un_reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=None,
                                                                         title="title", description="description",
                                                                         start_date=timezone.localize(
                                                                             datetime.datetime(2026, 1, 1, 18,
                                                                                               30)),
                                                                         end_date=timezone.localize(
                                                                             datetime.datetime(2026, 1, 1, 19,
                                                                                               30)))
        self.reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=self.reservatore,
                                                                      title="title", description="description",
                                                                      start_date=timezone.localize(
                                                                          datetime.datetime(2027, 1, 1, 18,
                                                                                            30)),
                                                                      end_date=timezone.localize(
                                                                          datetime.datetime(2027, 1, 1, 19,
                                                                                            30)))
        self.late_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=self.reservatore,
                                                                  title="title", description="description",
                                                                  start_date=
                                                                  tz.now().__add__(
                                                                      datetime.timedelta(minutes=5)),
                                                                  end_date=
                                                                  tz.now().__add__(
                                                                      datetime.timedelta(minutes=6)))

    def test_un_authorize_client(self):
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_consultant_time_id(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "10/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه زمان مشاوره موجود نیست"})

    def test_un_reserved_consultant_time(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "این ساعت هنوز رزرو نشده است"})

    def test_late_cancel_consultant_time(self):
        self.client.force_authenticate(self.secretary)
        response = self.client.delete(self.url + "3/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "به زمان مشاوره کمتر از 60 دقیقه مانده است"})

    def test_un_reservatore_consultant_cancel_consultant_time(self):
        foreign_user = UserProfile.objects.create(username="foreign_user", email="mohsen@gmail.com",
                                                  password="123456",
                                                  phone_number="09176273747", first_name="mohsen",
                                                  last_name="azarbad")
        self.client.force_authenticate(foreign_user)
        response = self.client.delete(self.url + "2/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این کار را ندارید"})

    def test_consultant_cancel_successfully(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ConsultantTime.objects.filter(id=2)[0].user, None)

    def test_reservatore_cancel_successfully(self):
        self.client.force_authenticate(self.reservatore)
        response = self.client.delete(self.url + "2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ConsultantTime.objects.filter(id=2)[0].user, None)


class PrivateCommentAndGradeTest(TestCase):
    def setUp(self):
        self.post_url = '/calendar/consultant-time/comment/'
        self.get_url = '/consultant/comment/'
        self.client = APIClient()
        self.consultant = ConsultantProfile.objects.create(username="consultant", user_type='Immigration',
                                                           phone_number="09184576125", first_name="hossein",
                                                           last_name="masoudi", email="test1@gmailcom",
                                                           password="123456",
                                                           certificate="111")
        self.reservatore = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")

        timezone = pytz.timezone('UTC')
        self.un_reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=None,
                                                                         title="title", description="description",
                                                                         start_date=timezone.localize(
                                                                             datetime.datetime(2026, 1, 1, 18,
                                                                                               30)),
                                                                         end_date=timezone.localize(
                                                                             datetime.datetime(2026, 1, 1, 19,
                                                                                               30)))
        self.reserved_consultant_time = ConsultantTime.objects.create(consultant=self.consultant, user=self.reservatore,
                                                                      title="title", description="description",
                                                                      start_date=timezone.localize(
                                                                          datetime.datetime(2027, 1, 1, 18,
                                                                                            30)),
                                                                      end_date=timezone.localize(
                                                                          datetime.datetime(2027, 1, 1, 19,
                                                                                            30)))
        # add 20 consultant times with comment and grade
        for count in range(20):
            ConsultantTime.objects.create(consultant=self.consultant, user=self.reservatore, title="title",
                                          start_date=timezone.localize(datetime.datetime(2030 + count, 1, 1, 18, 30)),
                                          end_date=timezone.localize(datetime.datetime(2030 + count, 1, 1, 19, 30)),
                                          user_grade=count % 5, user_comment="مشاوره‌ی خوبی بود", )

    def test_un_authorize_client(self):
        response = self.client.post(self.post_url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.get_url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_consultant_time_id_post_request(self):
        self.client.force_authenticate(self.reservatore)
        response = self.client.post(self.post_url + "100/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی زمان‌مشاوره صحیح نیست"})

    def test_un_reserve_consultant_time_post_request(self):
        self.client.force_authenticate(self.reservatore)
        response = self.client.post(self.post_url + self.un_reserved_consultant_time.id.__str__() + "/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما مجاز به این کار نیستید"})

    def test_not_reservator_consultant_time_post_request(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.post(self.post_url + self.reserved_consultant_time.id.__str__() + "/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما مجاز به این کار نیستید"})

    def test_comment_post_request_successfully(self):
        self.client.force_authenticate(self.reservatore)
        payload = {
            "user_grade": 5,
            "user_comment": "جلسه‌ی خوبی بود"
        }
        response = self.client.post(self.post_url + self.reserved_consultant_time.id.__str__() + "/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        consultant_time = ConsultantTime.objects.filter(id=self.reserved_consultant_time.id)[0]
        self.assertEqual(consultant_time.user_grade, 5)
        self.assertEqual(consultant_time.user_comment, "جلسه‌ی خوبی بود")
        self.assertIsNotNone(consultant_time.user_grade_date)
        self.assertEqual(consultant_time.consultant.count_of_all_comments, 1)
        self.assertEqual(consultant_time.consultant.satisfaction_percentage, 100)

    def test_invalid_consultant_id_get_request(self):
        self.client.force_authenticate(self.reservatore)
        response = self.client.get(self.get_url + "10000" + "/?page=1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی مشاور صحیح نیست"})

    def test_get_comments_successfully(self):
        self.client.force_authenticate(self.reservatore)
        response = self.client.get(self.get_url + self.consultant.username + "/?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)['results']), 10)