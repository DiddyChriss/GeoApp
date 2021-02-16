from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'api', GeoAPIView, basename='list')

urlpatterns = router.urls

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]