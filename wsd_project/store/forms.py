from django import forms
from .models import Game, Order

class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'price', 'link')

