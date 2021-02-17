import datetime
from test import *
from django.contrib.auth import get_user_model
from django.core.files import File

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from .models import *
from .serializers import *

User = get_user_model()

class GeoDRFAPITestCase(APITestCase):
    def setUp(self):
        self.user = User(username='testone')          # def user
        self.user.set_password('somepassword')
        self.user.save()

        self.geo = Geo.objects.create(
            pk=1,
            user=self.user,
            ip_address='94.254.145.12',
            location_data='some location data',

        )

        self.serializer_data = {
            'pk': 2,
            'user': self.user,
            'ip_address': '94.254.145.12',
            'location_data': 'seme_data',
        }

        self.serializer = GeoLocationSerializer(instance=self.geo)


    def test_models_acount(self):                                           # test single models
        geo = Geo.objects.count()
        user_count = User.objects.count()
        self.assertEqual(geo, 1)
        self.assertEqual(user_count, 1)

    def test_get_list(self):                                                # test list of items
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')   # authorization
        data = {
            'ip_address': self.geo.ip_address,
            }
        url = api_reverse("api:list-list")
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post(self):                                                    # test post
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')   # authorization
        data = {
            'ip_address': '37.248.139.45',
            }
        url = api_reverse("api:list-list")
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['ip_address'], self.serializer_data['ip_address'])
        self.assertEqual(set(data.keys()), set(['pk', 'user', 'ip_address', 'location_data']))



