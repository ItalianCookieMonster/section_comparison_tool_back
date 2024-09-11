from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100, null=True, blank=True)
