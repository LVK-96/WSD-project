from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name = 'index'),
    path('games', views.games, name = 'games'),
    path('highscores', views.highscores, name = 'highscores'),
    path('addgame', views.addgame, name = 'addgame')
]