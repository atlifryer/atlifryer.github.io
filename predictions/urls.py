# predictions/urls.py

from django.urls import path
from .views import GameListView, LeaderboardView, KnockoutStageView

urlpatterns = [
    path('games/', GameListView.as_view(), name='game_list'),
    path('knockout/<str:stage>/', KnockoutStageView.as_view(), name='knockout_stage'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]