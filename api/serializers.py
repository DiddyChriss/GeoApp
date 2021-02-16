import requests

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IPAddressField

from .models import *

class GeoLocationSerializer(ModelSerializer):
    pk = SerializerMethodField(read_only=True)
    user = SerializerMethodField(read_only=True)
    ip_address = IPAddressField()
    location_data = SerializerMethodField(read_only=True)

    class Meta:
        model = Geo
        fields = [
            'pk',
            'user',
            'ip_address',
            'location_data',
        ]

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Geo.objects.all(),
        #         fields=['ip_address',]
        #     )
        # ]

    def get_pk(self, obj):
        return obj.id

    def get_ip_address(self, obj):
        return str(obj.ip_address)

    def get_user(self, obj):
        return str(obj.user.username)

    def get_location_data(self, obj):
        url = f'http://api.ipstack.com/{obj.ip_address}?access_key=b5ee55e0869b57257386da06897b3655'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers)
        ip_list = response.text.strip('{').strip('}').replace('\"', '').split(sep=',')
        ip = dict([(x.strip(']').strip('}').split(sep=':')) for x in ip_list if 'flag' not in x and
                    'location' not in x and 'pl' not in x])
        return ip

    # def validate_ip_address(self, value):
    #     request = self.context.get("request")
    #     # user_id = self.get_user()
    #     print(self)
    #     if Geo.objects.filter(user=4, ip_address=value):
    #         raise serializers.ValidationError("This field must be unique.")
    #     return value