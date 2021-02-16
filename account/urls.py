from django.urls import path, include

# from rest_framework_simplejwt.token_blacklist.views import BlacklistView

from .views import *


app_name = 'account'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # path("logout/", BlacklistView.as_view({"post": "create"})),
]