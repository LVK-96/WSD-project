from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('store', views.store, name='store'),
    path('library', views.my_library, name='my_library'),
    path('library/startgame/<int:game_pk>', views.startgame, name='startgame'),
    path('devpanel', views.developer_panel, name='devpanel'),
    path('modify/<int:game_pk>/', views.dev_modify_game, name = 'modify'),
    path('highscores', views.highscores, name='highscores'),
    path('addgame', views.addgame, name='addgame'),
    path('cart', views.cart, name='cart'),
    path('payment/confirm', views.confirm_payment, name='confirm'),
    path('highscore/<int:game_pk>/<int:new_score>', views.addhighscore, name='highscore'),
    path('payment/success', views.payment_success, name='payment_success'),
    path('payment/cancel', views.payment_cancel, name='payment_cancel'),
    path('payment/error', views.payment_error, name='payment_error')
]