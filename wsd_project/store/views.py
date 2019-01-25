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
    if request.method == 'POST':
        request.session['cart'] = request.POST.get("id") 
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
    if 'cart' not in request.session:
        request.session['cart'] = ''
    
    user_cart = request.session['cart']
    user_cart.split(",")
    total = 0
    for game_id in user_cart:
        game = Game.objects.get(pk=game_id)
        total += game.price
    

    current_user = request.user
    print(request.session.session_key)
    print(total)
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(request.session.session_key, "wsd18store", total, "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = (md5(checksumstr.encode("ascii"))).hexdigest()
    return render(request, 'store/cart.html', {'checksum': checksum, 'total': total, 'cart_id': request.session.session_key})

def payment_success(request):
    #request.user.addgame
    #request.user.addorder 
    return render(request, 'store/payment_success.html')

def payment_cancel(request):
    return render(request, 'store/payment_cancel.html')

def payment_error(request):
    return render(request, 'store/payment_error.html')

#what other constraints are needed (cant add highscores without playing, the player actually owns the game)
#the game field in the highscores is a foreign key -> the primary key of the game
#a new highscore, with the minimum score should be added when a player purchases the game - this can be used
#to tell if a player has puirchased a specific game

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

@login_required
def startgame(request, game_pk):
    print(request.user, game_pk)
    print(Highscore.objects.all())
    if Highscore.objects.filter(player=request.user, game=game_pk):
        #if highscore exists the player owns the game
        print('highscore exists for player')
        game = Game.objects.get(pk=game_pk)
        return render(request, 'store/startgame.html', {'game' : game})
    else:
        print("redirected")
        #if highscore doesn't exist, the player doesn't own the game
        return redirect('my_library')#should it be mylibrary.html

