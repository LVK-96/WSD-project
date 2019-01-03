from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    return render(request, 'store/home.html')

def games(request):
    return render(request, 'store/games.html')

def highscores(request):
    return render(request, 'store/highscores.html')