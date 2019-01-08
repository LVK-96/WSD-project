from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser  

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'is_dev', 'profile_pic')

        labels = {
            'is_dev': 'Are you a developer?',
        }

class ChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')