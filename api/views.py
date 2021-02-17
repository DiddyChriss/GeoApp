from django.contrib import auth
from django.db import IntegrityError

from rest_framework import status, generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .serializers import *

class GeoAPIView(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet,):

    queryset = Geo.objects.all()
    serializer_class = GeoLocationSerializer
    # authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            geo = Geo.objects.get(user=request.user, ip_address=serializer.data['ip_address'])
            geo.location_data = serializer.data['location_data']
            geo.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
