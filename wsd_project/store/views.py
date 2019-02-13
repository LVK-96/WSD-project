''' Write views here '''
from hashlib import md5
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.views import generic
from .forms import NewGameForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Order, Highscore, Game
from django.conf import settings
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

@login_required
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
def developer_panel(request):
    if not request.user.isdev():
        return HttpResponseForbidden
    
    devs_games = Game.objects.filter(dev=request.user)
    return render(request, 'store/dev_panel.html', {'games': devs_games})

@login_required
def dev_modify_game(request, game_pk):
    check_game = Game.objects.get(pk=game_pk)
    owner = check_game.dev

    if not owner == request.user:
        return HttpResponseForbidden
    
    if request.method == 'GET':
        orders = Order.objects.filter(games=check_game)
        return render(request, 'store/modify_game.html', {'game': check_game, 'orders': orders})
    
    return redirect('devpanel')

@login_required
def cart(request):
    # payment service: http://payments.webcourse.niksula.hut.fi/
    if 'cart' not in request.session:
       request.session['cart'] = []
    
    user_cart = request.session['cart']
    empty_flag = False
    if not user_cart:
        empty_flag = True

    games = []
    prices = []
    total = 0
    for game_id in user_cart:
        game = Game.objects.get(pk=game_id)
        games.append(game)
        total += game.price
        prices.append(game.price)
    games_and_prices = zip(games, prices)
    
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(request.session.session_key, "wsd18store", total, "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    return render(request, 'store/cart.html', {'checksum': checksum, 'total': total, 'games_and_prices': games_and_prices, 'empty_flag': empty_flag})

@login_required
def confirm_payment(request):
    if 'cart' not in request.session:
        return redirect('cart')
    
    user_cart = request.session['cart']
    total = 0    
    for game_id in user_cart:
        game = Game.objects.get(pk=game_id)
        total += game.price
    
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(request.session.session_key, "wsd18store", total, "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    
    if request.method == 'POST':
        if checksum == request.POST.get("checksum"):
            order = Order.objects.create(user=request.user)
            user_cart = request.session['cart']
            order.total = total
            order.session_key = request.session.session_key
            for game_id in user_cart:
                game = Game.objects.get(pk=game_id)
                order.games.add(game)
            order.save()
            return render(request, 'store/confirm.html', {'checksum': checksum, 'total': total, 'cart_id': request.session.session_key, 'PAYMENT_SUCCESS_URL': settings.PAYMENT_SUCCESS_URL, 'PAYMENT_CANCEL_URL': settings.PAYMENT_CANCEL_URL, 'PAYMENT_ERROR_URL': settings.PAYMENT_ERROR_URL})
        return HttpResponseForbidden() 
    
    return render(request, 'store/home.html')

@login_required
def payment_success(request):
    # calculate checksum
    checksumstr = "pid={}&ref={}&result={}&token={}".format(request.session.session_key, request.GET.get("ref"), request.GET.get("result"), "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    if (checksum == request.GET.get("checksum") and request.GET.get("result") == "success"):
        # delete cart from session
        # set order status to succcess
        user_cart = request.session['cart']
        del request.session['cart']

        order = Order.objects.get(session_key=request.session.session_key)
        order.status = order.SUCCESFULL_PAYMENT
        order.save()
        
        # add games to user
        for game_id in user_cart:
            game = Game.objects.get(pk=game_id)
            highscore = Highscore(player=request.user, game=game)
            highscore.save()

        request.session.cycle_key()
        return render(request, 'store/payment_success.html')
    return HttpResponseForbidden()

@login_required
def payment_cancel(request):
    checksumstr = "pid={}&ref={}&result={}&token={}".format(request.session.session_key, request.GET.get("ref"), request.GET.get("result"), "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    if (checksum == request.GET.get("checksum") and request.GET.get("result") == "cancel"):
        user_cart = request.session['cart']
        del request.session['cart']

        order = Order.objects.get(session_key=request.session.session_key)
        order.status = order.CANCELED_PAYMENT
        order.save()

        request.session.cycle_key()
        return render(request, 'store/payment_cancel.html')
    return HttpResponseForbidden()

@login_required
def payment_error(request):
    checksumstr = "pid={}&ref={}&result={}&token={}".format(request.session.session_key, request.GET.get("ref"), request.GET.get("result"), "ad730b6cf25ef42d9cc48e2fbfa28a31")
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    if (checksum == request.GET.get("checksum") and request.GET.get("result") == "error"):
        user_cart = request.session['cart']
        del request.session['cart']

        order = Order.objects.get(session_key=request.session.session_key)
        order.status = order.FAILED_PAYMENT
        order.save()
        
        request.session.cycle_key()
        return render(request, 'store/payment_error.html')
    return HttpResponseForbidden()

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
            else:
                return HttpResponse(status=204)

        elif requesttype == "SAVE":
            newstate = request.POST.get('gamestate')
            highscoreobj = Highscore.objects.get(player=request.user, game=game_pk)
            print(newstate)
            highscoreobj.state = newstate
            highscoreobj.save() 
            return HttpResponse(status=204)

        elif requesttype == "LOAD":
            print(request.POST.get('score'))
            return HttpResponse(status=204)

        elif requesttype == "ERROR":
            print("error")
            return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)#400 bad request
    else:
        return redirect('my_library')