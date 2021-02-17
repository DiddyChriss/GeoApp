import requests

from rest_framework import serializers
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

    def get_pk(self, obj):
        if not str(obj.pk):
            raise serializers.ValidationError('pk does not exists!')
        return str(obj.pk)

    def get_user(self, obj):
        if not obj.user.username:
            raise serializers.ValidationError('user does not exists!')
        return str(obj.user.username)

    def get_location_data(self, obj):
        try:
            url = f'http://api.ipstack.com/{obj.ip_address}?access_key=b5ee55e0869b57257386da06897b3655'
            headers = {'Content-Type': 'application/json'}
            response = requests.get(url, headers)
            ip_list = response.text.strip('{').strip('}').replace('\"', '').split(sep=',')
            ip = dict([(x.strip(']').strip('}').split(sep=':')) for x in ip_list if 'flag' not in x and
                    'location' not in x and 'pl' not in x])
        except:
            ip = None
            raise serializers.ValidationError('upsss, something went wrong!')
        return ip

    def validate_ip_address(self, value):
        request = self.context.get("request")
        if Geo.objects.filter(user=request.user, ip_address=value):
            raise serializers.ValidationError(f"IP Address({value}) already in use by {request.user}")
        return value

