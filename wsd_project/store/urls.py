from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('games', views.games, name = 'games'),
    path('highscores', views.highscores, name = 'highscores'),
    path('addgame', views.AddGame.as_view(), name = 'addgame')
]