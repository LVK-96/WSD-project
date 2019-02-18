from django.shortcuts import render
from store.models import Highscore, Game
from users.models import CustomUser
from django.template import loader
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

        if username == None and game_name == None:
            return render(request, 'api/REST.html', {'jsonString': " "})

        if username != None and game_name != None:
            user = CustomUser.objects.get(username=username)
            game = Game.objects.get(name=game_name)
            if Highscore.objects.get(game=game, player=user):
                score_JSON = json.dumps(highscore.score)
                highscore = Highscore.objects.get(game=game, player=user)
                return render(request, 'api/REST.html', {'jsonString': score_JSON})

        if game_name == None:
            user = CustomUser.objects.get(username=username)
            if Highscore.objects.filter(player=user):
                games = []
                scores = []
                for highscore in Highscore.objects.filter(player=user):
                    games.append(highscore.game.name)
                    scores.append(highscore.score)
                games_and_scores = dict(zip(games, scores))
                games_and_scores_JSON = json.dumps(games_and_scores) 
                return render(request, 'api/REST.html', {'jsonString': games_and_scores_JSON})

        if username == None:
            game = Game.objects.get(name=game_name)
            if Highscore.objects.filter(game=game):
                users = []
                scores = []
                for highscore in Highscore.objects.filter(game=game):
                    users.append(highscore.player.username)
                    scores.append(highscore.score)
                users_and_scores = dict(zip(users, scores))
                users_and_scores_JSON = json.dumps(users_and_scores)
                return render(request, 'api/REST.html', {'jsonString': users_and_scores_JSON})
    
    return render(request, 'api/REST.html', {'jsonString': " "})