import os

from django.core.files.base import File
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json

from User.models import *


class PrivateUserProfileTest(TestCase):
    def setUp(self):
        self.url = "/consultant/search-consultants/"
        self.client = APIClient()
        self.consultant1 = ConsultantProfile.objects.create(username="test", phone_number="09184576125",
                                                           first_name="hossein", last_name="masoudi",
                                                           email="test1@gmailcom", password="123456",
                                                           certificate="111", user_type='Lawyer')
        self.consultant2 = ConsultantProfile.objects.create(username="consultant", user_type='Immigration',
                                                           phone_number="09184789625", first_name="hossein",
                                                           last_name="masoudi", email="mosoud@gmailcom",
                                                           password="123456", avatar="File(avatar)",
                                                           certificate="File(certificate)")
        self.consultant2 = ConsultantProfile.objects.create(username="ali", user_type='Immigration',
                                                           phone_number="09184574587", first_name="hosseini",
                                                           last_name="mahmoudiii", email="mahmoud@gmailcom",
                                                           password="24789632", avatar="File(avatar)",
                                                           certificate="File(certificate)")

    def test_get_all_consultant_sucessfully(self):
        response = self.client.get(self.url + '?query=&page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_get_out_of_size_page(self):
        response = self.client.get(self.url + '?query=&page=3')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    def test_get_queries(self):
        response = self.client.get(self.url + '?query=test&page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        response = self.client.get(self.url + '?query=&page=1&search_category=Immigration')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get(self.url + '?query=masoudi&page=1&search_category=Immigration')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    