from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    avatar_url = models.CharField(max_length=500, blank=True, null=True)
    registration_cookie = models.CharField(max_length=255, blank=True, null=True)
