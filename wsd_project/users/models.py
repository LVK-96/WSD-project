from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    # add additional fields in here
    is_dev = models.BooleanField(default = False)
    profile_pic = models.ImageField(default='default.png')
    bio = models.CharField(default='', max_length=500)
    

