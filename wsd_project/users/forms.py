'''
Forms for user signup and update
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class SignupForm(UserCreationForm):
    '''
    Form for user signup, profile created with signal in signals.py
    '''
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'is_dev')

        labels = {
            'is_dev': 'Are you a developer?',
        }

class ChangeForm(forms.ModelForm):
    '''
    Form for user update
    '''
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    '''
    Form for profile update
    '''
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']