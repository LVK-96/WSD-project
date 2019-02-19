''' Write views here '''
from hashlib import md5
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views import generic
from .forms import NewGameForm, GameUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order, Highscore, Game
from users.models import CustomUser
from django.conf import settings
from django.db.models.aggregates import Max
#from django.utils.decorators import method_decorator

user_login_required = user_passes_test(lambda user: user.is_active, login_url='/')
def active_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func

# Create your views here.
def index(request):
    return render(request, 'store/home.html')

def store(request):
    allgames = Game.objects.all()
    tags = Game.GENRE_CHOISES
    flag = 0

    if request.method == 'POST':
        if request.POST.get('messagetype') == 'cart':
            if 'cart' not in request.session:
                request.session['cart'] = []
            user_cart = request.session['cart']
            highscores = Highscore.objects.filter(game = Game.objects.get(pk = request.POST.get("id")), player = request.user)
            if request.POST.get("id") not in user_cart and not highscores: # No duplicate items in cart and user does not already own game
                user_cart.append(request.POST.get("id"))
            request.session['cart'] = user_cart
        elif request.POST.get('messagetype') == 'filter':
            tagstoshow = []
            for key, value in request.POST.items():
                #make the chosen tags into a list
                if(key != 'csrfmiddlewaretoken' and key != 'messagetype' and key != 'filter'):
                    tagstoshow.append(key)
            #filter allgames using the tags in the values
            allgames = allgames.filter(genre__in=tagstoshow)
        elif request.POST.get('messagetype') == 'search':
            #check if game with that name exists
            name = Game.objects.filter(name=request.POST.get('search'))
            if name:
                allgames = name
            else:
                #to tell the template that game with that name was not found
                flag = 1
            
    return render(request, 'store/store.html', {'allgames': allgames, 'tags': tags, 'flag': flag})

def highscores(request):
    if request.method == 'GET':
        if "game" in request.GET:
            game_name = request.GET.get("game")
            game = Game.objects.get(name=game_name)
            highscores = Highscore.objects.filter(game=game)
            return render(request, 'store/highscores.html', {'highscores': highscores, 'game': game})
    return render(request, 'store/highscores.html')

@active_user_required
def my_library(request):
    #In highscores foreign keys are saved as
    if request.user.is_dev:
        return redirect('index')
    myhighscores = Highscore.objects.filter(player_id=request.user.pk)
    allgames = Game.objects.all()
    return render(request, 'store/my_library.html', {'myhighscores': myhighscores, 'allgames': allgames})

@active_user_required
def addgame(request):
    if request.user.is_dev:
        if request.method == 'POST':
            form = NewGameForm(request.POST)
            if form.is_valid():
                game = form.save(commit = False)
                game.dev = request.user
                game.save()
                return redirect('devpanel')
        else:
            form = NewGameForm()

        return render(request, 'store/addgame.html', {'form': form})
    else:
        return redirect('devpanel')

@active_user_required
def developer_panel(request):
    if not request.user.is_dev:
        return HttpResponseForbidden

    devs_games = Game.objects.filter(dev=request.user)
    return render(request, 'store/dev_panel.html', {'games': devs_games})

@active_user_required
def order_history(request, game_pk):
    check_game = Game.objects.get(pk=game_pk)
    owner = check_game.dev

    if owner == request.user:
        orders = Order.objects.filter(games=check_game)
        dates = []
        prices = []
        for order in orders:
            for game_name, price in order.decodeJSON(order.games_and_prices).items():
                if (game_name == check_game.name):
                    dates.append(order.date)
                    prices.append(price)
        dates_and_prices = zip(dates, prices)
        return render(request, 'store/order_history.html', {'dates_and_prices': dates_and_prices, 'game': check_game})

    return HttpResponseForbidden

@active_user_required
def dev_modify_game(request, game_pk):
    check_game = Game.objects.get(pk=game_pk)
    owner = check_game.dev

    if owner == request.user:
        if request.method == 'POST':
            form = GameUpdateForm(request.POST, instance=check_game)
            if form.is_valid():
                form.save()
                return redirect('modify', game_pk=game_pk)
        else:
            form = GameUpdateForm(instance=check_game)
            return render(request, 'store/modify_game.html', {'form': form, 'game': check_game})

    return HttpResponseForbidden

@active_user_required
def cart(request):
    # payment service: http://payments.webcourse.niksula.hut.fi/
    if request.user.is_dev:
        return redirect('index')

    if 'cart' not in request.session:
       request.session['cart'] = []

    user_cart = request.session['cart']
    if request.method == 'POST':
        print("asd")
        game_id = request.POST.get("game_id")
        if game_id in user_cart:
            user_cart.remove(game_id)
            request.session['cart'] = user_cart
    
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

    checksumstr = "pid={}&sid={}&amount={}&token={}".format(request.session.session_key, settings.SID, total, settings.PAYMENT_TOKEN)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    return render(request, 'store/cart.html', {'checksum': checksum, 'total': total, 'games_and_prices': games_and_prices, 'empty_flag': empty_flag})

@active_user_required
def confirm_payment(request):
    if 'cart' not in request.session:
        return redirect('cart')

    user_cart = request.session['cart']
    total = 0
    for game_id in user_cart:
        game = Game.objects.get(pk=game_id)
        total += game.price

    checksumstr = "pid={}&sid={}&amount={}&token={}".format(request.session.session_key, settings.SID, total, settings.PAYMENT_TOKEN)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()

    if request.method == 'GET':
        if checksum == request.GET.get("checksum"):
            order = Order.objects.create(user=request.user)
            user_cart = request.session['cart']
            order.total = total
            order.session_key = request.session.session_key
            games = []
            prices = []
            for game_id in user_cart:
                game = Game.objects.get(pk=game_id)
                games.append(game.name)
                prices.append(game.price)
                order.games.add(game)
            games_and_prices = dict(zip(games, prices))
            order.games_and_prices = order.encodeJSON(games_and_prices)
            order.save()
            return render(request, 'store/confirm.html', {'checksum': checksum, 'total': total, 'cart_id': request.session.session_key, 'PAYMENT_SUCCESS_URL': settings.PAYMENT_SUCCESS_URL, 'PAYMENT_CANCEL_URL': settings.PAYMENT_CANCEL_URL, 'PAYMENT_ERROR_URL': settings.PAYMENT_ERROR_URL})
        return HttpResponseForbidden()

    return redirect('index')

@active_user_required
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

@active_user_required
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

@active_user_required
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


@active_user_required
def startgame(request, game_pk):
    if request.user.is_dev:
        return redirect('index')

    if request.method == 'GET':
        if Highscore.objects.filter(player=request.user, game=game_pk):
            #if highscore exists the player owns the game
            game = Game.objects.get(pk=game_pk)
            return render(request, 'store/startgame.html', {'game' : game})
        else:
            #if highscore doesn't exist, the player doesn't own the game
            return redirect('my_library')#should it be mylibrary.html

    if request.method == 'POST':
        #test that user owns the game
        if Highscore.objects.filter(player=request.user, game=game_pk):
            #ajax request so the html response isn't rendered
            requesttype = request.POST.get('messagetype')
            highscoreobj = Highscore.objects.get(player=request.user, game=game_pk)

            if requesttype == "SCORE":
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
                highscoreobj.state = newstate
                highscoreobj.save()
                return HttpResponse(status=204)

            elif requesttype == "LOAD_REQUEST":
                return JsonResponse({'state': highscoreobj.state})

            elif requesttype == "ERROR":
                return HttpResponse(status=400)
            else:
                return HttpResponse(status=400)#400 bad request
        else:
            redirect('my_library')
    else:
        return redirect('my_library')


def game_description(request, game_pk):
    if request.method == 'GET':
        try:
            game = Game.objects.get(pk=game_pk)
            tophighscores = Highscore.objects.filter(game = game)
            tophighscores.order_by('score')
            tophighscores = tophighscores[:10]
            return render(request, 'store/gamedescription.html', {'game' : game, 'tophighscores': tophighscores})
        except:
            return redirect('store')
