# predictions/urls.py

from django.urls import path
from .views import GameListView, LeaderboardView, KnockoutRoundView

urlpatterns = [
    path('games/', GameListView.as_view(), name='game_list'),
    path('knockout/<str:round>/', KnockoutRoundView.as_view(), name='knockout_round'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]