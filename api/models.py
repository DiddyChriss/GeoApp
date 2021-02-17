from django.contrib.auth.models import User
from django.db import models

class Geo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip_address = models.CharField(max_length=25, null=True)
    location_data = models.TextField(max_length=5000, null=True)

    def __str__(self):
        return str(f'{self.user}, {self.ip_address}')



