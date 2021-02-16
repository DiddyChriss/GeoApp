from django.shortcuts import render
from django.contrib.auth import login

from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth.models import User

from .models import *
from .serializers import *


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    # def post(self, request, *args,  **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     return Response({
    #         "user": UserSerializer(user,    context=self.get_serializer_context()).data,
    #         "message": "User Created Successfully.  Now perform Login to get your token",
    #     })

class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    custom_serializer_classes = MyTokenObtainPairSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)