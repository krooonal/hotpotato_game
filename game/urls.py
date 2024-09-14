# game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game),
    path('pass/', views.pass_potato),
]
