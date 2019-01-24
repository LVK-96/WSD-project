from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from .forms import NewGameForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from hashlib import md5
from .models import Order
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
    if request.user.isdev():
        if request.method == 'POST':
            form = NewGameForm(request.POST)
            if form.is_valid():
                game = form.save(commit = False)
                game.dev = request.user
                game.save()

                return redirect('profilepage')
        else:
            form = NewGameForm()
    
        return render(request, 'store/addgame.html', {'form': form})
    else:
        return redirect('profilepage')

@login_required
def cart(request):
    # payment service: http://payments.webcourse.niksula.hut.fi/
    if Order.objects.filter(player=request.user).exists():
        order = Order.objects.get(player_id=request.user.id)
    else:
        order = Order.objects.create(player=request.user)

    checksumstr = "pid={}&sid={}&amount={}&token={}".format(order.id, "wsd18store", order.total, "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = (md5(checksumstr.encode("ascii"))).hexdigest()
    return render(request, 'store/cart.html', {'checksum': checksum, 'order': order})