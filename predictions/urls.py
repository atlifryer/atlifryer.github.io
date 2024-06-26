# predictions/urls.py

from django.urls import path
from .views import GameListView, LeaderboardView, KnockoutGameListView, AdvanceRoundView

urlpatterns = [
    path('games/', GameListView.as_view(), name='game_list'),
    path('knockout-games/', KnockoutGameListView.as_view(), name='knockout_game_list'),
    path('advance-round/<int:round_number>/', AdvanceRoundView.as_view(), name='advance_round'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]