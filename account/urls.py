from django.urls import path, include

from .views import *


app_name = 'account'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenLogoutView.as_view(), name='logout'),
]