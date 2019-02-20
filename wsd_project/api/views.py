from django.shortcuts import render
from store.models import Highscore, Game
from users.models import CustomUser
from django.template import loader
from django.http import JsonResponse
import json
# Create your views here.
def RESTapi(request):
    if request.method == 'GET':
        if 'username' in request.GET:
            username = request.GET.get("username")
        else:
            username = None
        
        if 'game' in request.GET:
            game_name = request.GET.get("game")
        else:
            game_name = None

        print(username)
        print(game_name) 

        if username == None and game_name == None:
            return JsonResponse({})

        if username != None and game_name != None:
            if CustomUser.objects.filter(username=username):
                user = CustomUser.objects.get(username=username)
            else:
                return JsonResponse({})
            
            if Game.objects.filter(name=game_name):
                game = Game.objects.get(name=game_name)
            else:
                return JsonResponse({})

            if Highscore.objects.get(game=game, player=user):
                highscore = Highscore.objects.get(game=game, player=user)
                ret = {username: highscore.score}
                return JsonResponse(ret)

        if game_name == None:
            if CustomUser.objects.filter(username=username):
                user = CustomUser.objects.get(username=username)
            else:
                return JsonResponse({})
            
            if Highscore.objects.filter(player=user):
                games = []
                scores = []
                for highscore in Highscore.objects.filter(player=user):
                    games.append(highscore.game.name)
                    scores.append(highscore.score)
                games_and_scores = dict(zip(games, scores))
                return JsonResponse(games_and_scores)

        if username == None:
            if Game.objects.filter(name=game_name):
                game = Game.objects.get(name=game_name)
            else:
                return JsonResponse({})
            
            if Highscore.objects.filter(game=game):
                users = []
                scores = []
                for highscore in Highscore.objects.filter(game=game):
                    users.append(highscore.player.username)
                    scores.append(highscore.score)
                users_and_scores = dict(zip(users, scores))
                return JsonResponse(users_and_scores)
    
    return JsonResponse({})