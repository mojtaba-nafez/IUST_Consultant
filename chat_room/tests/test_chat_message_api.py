import os

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json
from django.core.files.base import File

from User.models import UserProfile, ConsultantProfile
from message.models import ChatMessage


class PrivateChatMessageTest(TestCase):
    def setUp(self):
        self.url = "/chat/direct/message/"
        self.client = APIClient()
        self.consultant = ConsultantProfile.objects.create(username="consultant", user_type='Immigration',
                                                           phone_number="09184576125", first_name="hossein",
                                                           last_name="masoudi", email="test1@gmailcom",
                                                           password="123456",
                                                           certificate="111")
        self.normal_user = UserProfile.objects.create(username="normal_user", email="hamid@gmail.com",
                                                      password="123456",
                                                      phone_number="09176273746", first_name="hamid",
                                                      last_name="azarbad")
        self.forbidden_user = UserProfile.objects.create(username="forbidden", email="reza@gmail.com",
                                                         password="123456",
                                                         phone_number="09176273745", first_name="reza",
                                                         last_name="rezaee")
        self.chat_message = ChatMessage.objects.create(text="Hello", message_type="t", message_file=None,
                                                       sender=self.consultant, receiver=self.normal_user, )

    def test_un_authorize_client(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_receiver_id_post_chat_message(self):
        self.client.force_authenticate(self.consultant)
        payload = {
            "text": "GoodBy",
            "message_type": "t",
            "receiver_id": 10,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه دریافت‌کننده درست نیست"})

    def test_not_consultant_in_message_post_chat_message(self):
        self.client.force_authenticate(self.normal_user)
        payload = {
            "text": "GoodBy",
            "message_type": "t",
            "receiver_id": 2,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "یک سمت‌پیام باید مشاور باشد"})

    def test_post_chat_message_successfully(self):
        self.client.force_authenticate(self.consultant)
        payload = {
            "text": "GoodBy",
            "message_type": "t",
            "receiver_id": 2,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
            'id': 2,
            "text": "GoodBy",
            "message_type": "t",
            "message_file": None
        })

    def test_invalid_chat_message_id_get_chat_message(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url + "10/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی پیام صحیح نیست"})

    def test_forbidden_get_chat_message(self):
        self.client.force_authenticate(self.forbidden_user)
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این پیام را ندارید"})

    def test_get_chat_message_successfully(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {"id": 1, "text": "Hello", "message_type": "t", "message_file": None})
        self.client.force_authenticate(self.consultant)
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {"id": 1, "text": "Hello", "message_type": "t", "message_file": None})

    def test_invalid_chat_message_id_put_chat_message(self):
        self.client.force_authenticate(self.consultant)
        payload = {
            "text": "GoodBy",
            "message_type": "i"
        }
        response = self.client.put(self.url + "10/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه‌ی پیام صحیح نیست"})

    def test_forbidden_put_chat_message(self):
        self.client.force_authenticate(self.forbidden_user)
        payload = {
            "text": "GoodBy",
            "message_type": "i"
        }
        response = self.client.put(self.url + "1/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این پیام را ندارید"})
        self.client.force_authenticate(self.normal_user)
        response = self.client.put(self.url + "1/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این پیام را ندارید"})

    def test_put_chat_message_successfully(self):
        self.client.force_authenticate(self.consultant)
        file = File(open(os.path.dirname(__file__) + "/files/test.png", 'rb'))
        payload = {
            "text": "GoodBy",
            "message_type": "i",
            "message_file": file,
            "receiver_id": 1,
        }
        response = self.client.put(self.url + "1/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),"پیام بروز‌شد")
        chat_message = ChatMessage.objects.filter(id=1)[0]
        self.assertEqual(chat_message.text, "GoodBy")
        self.assertEqual(chat_message.message_type, "i")
        self.assertIsNotNone(chat_message.message_file)

    def test_invalid_chat_message_id_delete_chat_message(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "10/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "شناسه پیام صحیح نیست"})

    def test_forbidden_delete_chat_message(self):
        self.client.force_authenticate(self.forbidden_user)
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این‌کار ندارید"})
        self.client.force_authenticate(self.normal_user)
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"error": "شما دسترسی به این‌کار ندارید"})

    def test_delete_chat_message_successfully(self):
        self.client.force_authenticate(self.consultant)
        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),"پیام حذف شد")



