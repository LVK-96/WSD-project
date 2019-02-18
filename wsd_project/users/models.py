from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    # add additional fields in here
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, unique=True ,null=True, max_length=150)
    is_dev = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.CharField(default='', max_length=500)