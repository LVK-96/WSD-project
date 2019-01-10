from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    # add additional fields in here
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, unique=True ,null=True, max_length=150)
    is_dev = models.BooleanField(default = False)
    def isdev(self):
        if (self.is_dev):
            return True
        else:
            return False

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.CharField(default='', max_length=500)