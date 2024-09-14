# game/urls.py
from django.urls import path
from game.views import index
# from game.views import start_game, pass_potato, index

urlpatterns = [
    path('', index),
    # path('start/', start_game),
    # path('pass/', pass_potato),
]
