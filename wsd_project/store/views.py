''' Write views here '''
from hashlib import md5
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from .forms import NewGameForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Order, Highscore, Game
#from django.utils.decorators import method_decorator

# Create your views here.
def index(request):
    return render(request, 'store/home.html')

def store(request):
    return render(request, 'store/store.html')

def highscores(request):
    return render(request, 'store/highscores.html')

def my_library(request):
    return render(request, 'store/my_library.html')

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


def payment_success(request):
    return render(request, 'store/payment_success.html')

def payment_cancel(request):
    return render(request, 'store/payment_cancel.html')

def payment_error(request):
    return render(request, 'store/payment_error.html')

#what other constraints are needed (cant add highscores without playing, the player actually owns the game)
#the game field in the highscores is a foreign key -> the primary key of the game
@login_required
def addhighscore(request, game_pk, new_score):
    if request.method == 'POST':
        if Highscore.objects.filter(player=request.user, game=game_pk):
            #if highscore already exists, update it
            highscores = Highscore.objects.get(player=request.user, game=game_pk)
        else:
            #if highscore doesn't exist, create one
            Highscore.objects.create(game=game_pk, player = request.user, score = new_score)
        return redirect('profilepage')
         
