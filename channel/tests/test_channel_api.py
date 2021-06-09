from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from channel.models import Channel, Subscription
from User.models import ConsultantProfile, UserProfile

# SEARCH_CHANNEL = reverse()
class PublicSearchForChannelTests(TestCase):
    """Test unauthenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()
        consultant1=ConsultantProfile.objects.create(username="test",user_type='Immigration', phone_number="09184576125", first_name="hossein", last_name="masoudi", email="test1@gmailcom", password="qwertyu", certificate="111")
        ch1=Channel.objects.create(name="Test",description= "immegrate to UK", invite_link='test-link', consultant=consultant1)        
        consultant2=ConsultantProfile.objects.create(username="alialipour", user_type='Psychology', phone_number="09184526798", first_name="ali", last_name="alipour", email="test2@gmailcom", password="bvcxz", certificate="3333")
        ch2=Channel.objects.create(name="mamad",description= "join and win the Court", invite_link='UK-Imagrate', consultant=consultant2)
        consultant3=ConsultantProfile.objects.create(username="amin", user_type='Immigration', phone_number="09185762564", first_name="amini", last_name="masoudpour", email="amin@gmailcom", password="09876509ll", certificate="2586")
        ch3=Channel.objects.create(name="rasoul",description= "immegrate to Germany", invite_link='Immigrate-Germany', consultant=consultant3)        


    def test_get_all_object_in_category(self):
        """ test when query in query parameter is set to '' => output is all object in category """
        res = self.client.get('/channel/search-for-channel/?query=&search_category=Immigration')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_get_all_object_in_query(self):
        """ test when category not exist  => output is all general search """
        res = self.client.get('/channel/search-for-channel/?query=to')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        

    def test_check_search_in_channel_name(self):
        """ check search in name """
        res = self.client.get('/channel/search-for-channel/?query=soul&search_category=Immigration')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
    
    def test_check_search_in_channel_description(self):
        """ check search in description """
        res = self.client.get('/channel/search-for-channel/?query=win&search_category=Psychology')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
    
class SuggestionChannelTests(TestCase):
    """Test unauthenticated recipe API access"""
    def setUp(self):
        
        self.client = APIClient()
        consultant1=ConsultantProfile.objects.create(username="test",user_type='Immigration', phone_number="09184576125", first_name="hossein", last_name="masoudi", email="test1@gmailcom", password="qwertyu", certificate="111")
        ch1=Channel.objects.create(name="Test",description= "immegrate to UK", invite_link='test-link', consultant=consultant1)        
        consultant2=ConsultantProfile.objects.create(username="alialipour", user_type='Psychology', phone_number="09184526798", first_name="ali", last_name="alipour", email="test2@gmailcom", password="bvcxz", certificate="3333")
        ch2=Channel.objects.create(name="mamad",description= "join and win the Court", invite_link='UK-Imagrate', consultant=consultant2)
        consultant3=ConsultantProfile.objects.create(username="amin", user_type='Immigration', phone_number="09185762564", first_name="amini", last_name="masoudpour", email="amin@gmailcom", password="09876509ll", certificate="2586")
        ch3=Channel.objects.create(name="rasoul",description= "immegrate to Germany", invite_link='Immigrate-Germany', consultant=consultant3)        

    def test_get_suggession_successfully(self):
        res = self.client.get('/channel/suggestion-channel/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['Immigration']), 2)

class ChannelSubscriberTests(TestCase):
    """ admin get channel subscriber """
    def setUp(self):
        self.un_authorize_client = APIClient()

        consultant1=ConsultantProfile.objects.create(username="test",user_type='Immigration', phone_number="09184576125", first_name="hossein", last_name="masoudi", email="test1@gmailcom", password="qwertyu", certificate="111")
        ch1=Channel.objects.create(name="Test",description= "immegrate to UK", invite_link='test-link', consultant=consultant1)        
        consultant2=ConsultantProfile.objects.create(username="amin", user_type='Immigration', phone_number="09185762564", first_name="amini", last_name="masoudpour", email="amin@gmailcom", password="09876509ll", certificate="2586")
        ch2=Channel.objects.create(name="rasoul",description= "immegrate to Germany", invite_link='Immigrate-Germany', consultant=consultant2)        
        consultant3=ConsultantProfile.objects.create(username="alialipour", user_type='Psychology', phone_number="09184526798", first_name="ali", last_name="alipour", email="test2@gmailcom", password="bvcxz", certificate="3333")
        ch3=Channel.objects.create(name="mamad",description= "join and win the Court", invite_link='UK-Imagrate', consultant=consultant3)
        user1 = UserProfile.objects.create(username="reza", email="reza@gmail.com", password="12345qw", phone_number="09176273745",first_name="reza", last_name="rezaee")
        user2 = UserProfile.objects.create(username="ahamd", email="ahamd@gmail.com", password="1546145", phone_number="09176292744",first_name="ahamd", last_name="ahamdi")
        user3 = UserProfile.objects.create(username="akbar", email="akbar@gmail.com", password="vfdwsxd", phone_number="09178761538",first_name="akbar", last_name="akbari")
        user4 = UserProfile.objects.create(username="amir", email="amir@gmail.com", password="cdgfbbv", phone_number="09176274598",first_name="amir", last_name="amiri")
        Subscription.objects.create(channel=ch3, user=user1)
        Subscription.objects.create(channel=ch3, user=user2)
        Subscription.objects.create(channel=ch3, user=user3)
        Subscription.objects.create(channel=ch3, user=user4)
        
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(consultant3)
    
    def test_un_authorized_client_get_client(self):
        res=self.un_authorize_client.get("/channel/channel-subscriber/3/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_channel_3_admin_get_channel_1_subscriber(self):
        res=self.authorized_client.get("/channel/channel-subscriber/1/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    def test_get_channel_subscriber_successfully(self):
        res=self.authorized_client.get("/channel/channel-subscriber/3/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['data']), 4)

    def test_delete_subscriber_succesfully(self):
        payload = {
            'username': 'akbar'
        }
        res=self.authorized_client.delete('/channel/channel-subscriber/3/', payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    def test_delete_subscriber_with_wrong_username(self):
        payload = {
            'username': 'dlsfka'
        }
        res=self.authorized_client.delete('/channel/channel-subscriber/3/', payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    def test_delete_subscriber_serializer_error(self):
        payload = {
            'usefrname': 'dlsfka'
        }
        res=self.authorized_client.delete('/channel/channel-subscriber/3/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    def test_channel_3_admin_delete_channel_1_subscriber(self):
        payload = {
            'username': 'abbas'
        }
        res=self.authorized_client.delete('/channel/channel-subscriber/1/', payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    def test_un_auth_user_delete_subscriber(self):
        payload = {
            'username': 'akbar'
        }
        res=self.un_authorize_client.delete('/channel/channel-subscriber/3/', payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class GetChannelAdminTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        consultant=ConsultantProfile.objects.create(username="alialipour", user_type='Psychology', phone_number="09184526798", first_name="ali", last_name="alipour", email="test2@gmailcom", password="bvcxz", certificate="3333")
        ch=Channel.objects.create(name="mamad",description= "join and win the Court", invite_link='UK-Imagrate', consultant=consultant)
        user1 = UserProfile.objects.create(username="reza", email="reza@gmail.com", password="12345qw", phone_number="09176273745",first_name="reza", last_name="rezaee")
        user2 = UserProfile.objects.create(username="ahamd", email="ahamd@gmail.com", password="1546145", phone_number="09176292744",first_name="ahamd", last_name="ahamdi")
        user3 = UserProfile.objects.create(username="akbar", email="akbar@gmail.com", password="vfdwsxd", phone_number="09178761538",first_name="akbar", last_name="akbari")
        user4 = UserProfile.objects.create(username="amir", email="amir@gmail.com", password="cdgfbbv", phone_number="09176274598",first_name="amir", last_name="amiri")
        consultant.my_secretaries.add(user1)
        consultant.my_secretaries.add(user2)
        consultant.my_secretaries.add(user3)
        consultant.my_secretaries.add(user4)

    def test_get_channel_admin_successfully(self):
        res = self.client.get("/channel/channel-admins/1/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['data']['admin']), 4)

    def test_channel_not_exit(self):
        res = self.client.get("/channel/channel-admins/48545/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class EditChannelTests(TestCase):
    def setUp(self):
        self.un_authorized_client = APIClient()
        consultant1=ConsultantProfile.objects.create(username="test",user_type='Immigration', phone_number="09184576125", first_name="hossein", last_name="masoudi", email="test1@gmailcom", password="qwertyu", certificate="111")
        ch1=Channel.objects.create(name="Test",description= "immegrate to UK", invite_link='test-link', consultant=consultant1)        
        consultant2=ConsultantProfile.objects.create(username="alialipour", user_type='Psychology', phone_number="09184526798", first_name="ali", last_name="alipour", email="test2@gmailcom", password="bvcxz", certificate="3333")
        ch2=Channel.objects.create(name="mamad",description= "join and win the Court", invite_link='UK-Imagrate', consultant=consultant2)
        consultant3=ConsultantProfile.objects.create(username="amin", user_type='Immigration', phone_number="09185762564", first_name="amini", last_name="masoudpour", email="amin@gmailcom", password="09876509ll", certificate="2586")
        ch3=Channel.objects.create(name="rasoul",description= "immegrate to Germany", invite_link='Immigrate-Germany', consultant=consultant3)        
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(consultant3)
    
    def test_edit_channel_successfully(self):
        payload = {
            'description': 'TestTest',
            'invite_link': "TestTestTest",
            'name':"TestTestTestTestTest"
        }
        channel_befor_update = Channel.objects.get(pk=3)
        res = self.authorized_client.put("/channel/update-channel-inf/3/", payload)
        channel_after_update = Channel.objects.get(pk=3)
        self.assertEqual(channel_after_update.description, payload['description'])
        self.assertEqual(channel_after_update.invite_link, payload['invite_link'])
        self.assertEqual(channel_after_update.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_un_auth_user_access(self):
        payload = {
            'description': 'TestTest',
            'invite_link': "TestTestTest",
            'name':"TestTestTestTestTest"
        }
        channel_befor_update = Channel.objects.get(pk=3)
        res = self.un_authorized_client.put("/channel/update-channel-inf/3/", payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_channel_1_change_inf_channel_3(self):
        usr = ConsultantProfile.objects.get(pk=1)
        self.un_authorized_client.force_authenticate(usr)
        payload = {
            'description': 'TestTest',
            'invite_link': "TestTestTest",
            'name':"TestTestTestTestTest"
        }
        res = self.un_authorized_client.put("/channel/update-channel-inf/3/", payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
