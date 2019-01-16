from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from .forms import NewGameForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from hashlib import md5
#from django.utils.decorators import method_decorator

from .models import Game

# Create your views here.
def index(request):
    return render(request, 'store/home.html')

def games(request):
    return render(request, 'store/games.html')

def highscores(request):
    return render(request, 'store/highscores.html')

#add a login required decorator
@login_required
def addgame(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profilepage')
    else:
        form = NewGameForm(instance=request.user)
    
    return render(request, 'store/addgame.html', {'form': form})

@login_required
def cart(request):
    # payment service: http://payments.webcourse.niksula.hut.fi/
    if request.method == 'POST':
        form = CartForm(request.POST, instance=request.user)
        if form.is_valid:
            #calculate checksum
            checksumstr = "pid={}&sid={}&amount={}&token={}".format(request.user.order.id, "wsd18store", request.user.order.total, "ad730b6cf25ef42d9cc48e2fbfa28a31")
            checksum = (md5(checksumstr.encode("ascii"))).hexdigest()
            form.save()
