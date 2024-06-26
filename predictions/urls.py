# predictions/urls.py

from django.urls import path
from .views import GameListView, LeaderboardView

urlpatterns = [
    path('games/', GameListView.as_view(), name='game_list'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]