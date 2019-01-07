from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'is_dev')

        labels = {
            'is_dev': 'Are you a developer?',
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')