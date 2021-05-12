from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from channel.models import Channel
from User.models import ConsultantProfile, UserProfile
from calendar_.models import ConsultantTime
class PrivateReservationTests(TestCase):
    """Test Reservation Process"""
    
    def setUp(self): 
        self.client = APIClient()
        self.consultant=ConsultantProfile.objects.create(username="test", phone_number="09184576125", first_name="hossein", last_name="masoudi", email="test1@gmailcom", password="qwertyu", certificate="111", user_type='Immigration')
        ConsultantTime.objects.create(consultant=self.consultant, start_date="2021-05-08 06:52:38", end_date="2021-05-08 07:52:40")
        self.channel=Channel.objects.create(name="Test",description= "immegrate to UK", invite_link='test-link', consultant=self.consultant)        
        self.user = UserProfile.objects.create(username="reza", email="reza@gmail.com", password="12345qw", phone_number="09176273745",first_name="reza", last_name="rezaee")

    #####################################################################
    #####################################################################
    #####################################################################

    """ test  /calendar/reserve/<int:ConsultantID>/    get   request :    """

    def test_get_consultant_reservation_time_successfully(self):
        self.client.force_authenticate(self.user)
        res = self.client.get('/calendar/reserve/8/?date=2021-5-8')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_consultant_reservation_time_unauthenticated_user(self):
        res = self.client.get('/calendar/reserve/8/?date=2021-5-8')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_conultatn_reservation_time_incorrect_date_format(self):
        self.client.force_authenticate(self.user)
        res = self.client.get('/calendar/reserve/8/?date=2021/5/8')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data , "Incorrect date format, should be YYYY-MM-DD")
    def test_







    #####################################################################
    #####################################################################
    #####################################################################

    """ test  /calendar/reserve/<int:ConsultantID>/    post   request :    """

    def test_reserved_succeeds(self):
        """ test when query is set to '' => output is all object in category """
        self.client.force_authenticate(self.user)
        body = {
            "start_date": "2021-05-08 06:52:38+00:00",
            "end_date": "2021-05-08 07:52:40",
            "title": "test session",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    def test_consultant_not_have_empty_time(self):
        self.client.force_authenticate(self.user)
        body = {
            "start_date": "2021-08-02 06:52:38",
            "end_date": "2021-08-02 07:52:40",
            "title": "test session",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.data, "this consultant is busy in this time.")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    def test_time_reserved_before(self):
        self.client.force_authenticate(self.user)
        body = {
            "start_date": "2021-05-08 06:52:38",
            "end_date": "2021-05-08 07:52:40",
            "title": "test session",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        usr = UserProfile.objects.create(username="ahmad", email="admd@gmail.com", password="adsfrew32", phone_number="09176271258",first_name="ahmad", last_name="ahmadi")
        self.client.force_authenticate(usr)
        body = {
            "start_date": "2021-05-08 06:52:38",
            "end_date": "2021-05-08 07:52:40",
            "title": "test session",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data, "this consultant is busy in this time.")
    def test_reserved_wrong_consultantID(self):
        """ test when query is set to '' => output is all object in category """
        self.client.force_authenticate(self.user)
        body = {
            "start_date": "2021-05-08 06:52:38",
            "end_date": "2021-05-08 07:52:40",
            "title": "test session",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/34/', body)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)      
    def test_reserved_authenticated_user(self):
        """ test when query is set to '' => output is all object in category """
        body = {
            "start_date": "2021-05-08 06:52:38",
            "end_date": "2021-05-08 07:52:40",
            "title": "test session",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_bad_request_body_format(self):
        self.client.force_authenticate(self.user)
        "description format Error"
        body = {
            "start_date": "2021-05-08 06:52:38",
            "title": "test session",
            "end_date": "2021-05-08 07:52:40",
            "descriptionf": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        "title format Error"
        body = {
            "start_date": "2021-05-08 06:52:38",
            "end_date": "2021-05-08 07:52:40",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        "incorrect date format"
        body = {
            "start_date": "2021/05/08 06:52:38",
            "end_date": "2021-05-08 07:52:40",
            "title": "test session",
            "description": "resolve conflict"
        }
        res = self.client.post('/calendar/reserve/1/', body)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    