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
    allgames = Game.objects.all()
    response = render(request, 'store/store.html', {'allgames': allgames})
    if request.method == 'POST':
        if 'cart' not in request.session:
            request.session['cart'] = []
        user_cart = request.session['cart']
        highscores = Highscore.objects.filter(game = Game.objects.get(pk = request.POST.get("id")), player = request.user)
        if request.POST.get("id") not in user_cart and not highscores: # No duplicate items in cart and user does not already own game
            user_cart.append(request.POST.get("id"))
        request.session['cart'] = user_cart
    return response

def highscores(request):
    return render(request, 'store/highscores.html')

def my_library(request):
    #In highscores foreign keys are saved as
    myhighscores = Highscore.objects.filter(player_id=request.user.pk)
    allgames = Game.objects.all()
    return render(request, 'store/my_library.html', {'myhighscores': myhighscores, 'allgames': allgames})

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
       request.session['cart'] = []
    
    user_cart = request.session['cart']
    games = []
    prices = []
    total = 0
    for game_id in user_cart:
        game = Game.objects.get(pk=game_id)
        games.append(game)
        total += game.price
        prices.append(game.price)
    
    games_and_prices = zip(games, prices)
    current_user = request.user
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(request.session.session_key, "wsd18store", total, "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    return render(request, 'store/cart.html', {'checksum': checksum, 'total': total, 'cart_id': request.session.session_key, 'games_and_prices': games_and_prices})

def payment_success(request):
    # calculate checksum
    checksumstr = "pid={}&ref={}&result={}&token={}".format(request.session.session_key, request.GET.get("ref"), request.GET.get("result"), "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    if (checksum == request.GET.get("checksum")):
        # delete cart from session
        # add order to db
        # add games to user
        order = Order.objects.create(user=request.user)
        user_cart = request.session['cart']
        order_total = 0
        del request.session['cart']
        for game_id in user_cart:
            game = Game.objects.get(pk=game_id)
            highscore = Highscore(player=request.user, game=game)
            highscore.save()
            order_total += game.price
            order.games.add(game)
        order.total = order_total
        order.save()
        return render(request, 'store/payment_success.html')
    return render(request, 'store/payment_error.html')

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
            # TODO: fix this 
            highscores = Highscore.objects.get(player=request.user, game=game_pk)
        else:
            #if highscore doesn't exist, create one
            Highscore.objects.create(game=game_pk, player = request.user, score = new_score)
    return redirect('profilepage')

@login_required
def startgame(request, game_pk):

    if request.method == 'GET':
        if Highscore.objects.filter(player=request.user, game=game_pk):
            #if highscore exists the player owns the game
            game = Game.objects.get(pk=game_pk)
            return render(request, 'store/startgame.html', {'game' : game})
        else:
            #if highscore doesn't exist, the player doesn't own the game
            return redirect('my_library')#should it be mylibrary.html

    if request.method == 'POST':
        #ajax request so the html response isn't rendered
        requesttype = request.POST.get('messagetype')

        if requesttype == "SCORE":
            highscoreobj = Highscore.objects.get(player=request.user, game=game_pk)

            newscore = int(request.POST.get('score'))
            currentscore = highscoreobj.score
            if newscore > currentscore:
                highscoreobj.score = newscore
                highscoreobj.save()
                return HttpResponse(status=204)#204 request processed, but no content

        elif requesttype == "SAVE":
            print(request.POST.get('score'))
            return HttpResponse(status=204)

        elif requesttype == "LOAD":
            print(request.POST.get('score'))
            return HttpResponse(status=204)

        elif requesttype == "ERROR":
            print(request.POST.get('score'))
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)#400 bad request
    else:
        return redirect('my_library')
        

    

