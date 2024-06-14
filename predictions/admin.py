from django.contrib import admin
from .models import Game, Prediction

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'game_date')
    list_filter = ('game_date',)
    search_fields = ('team1', 'team2',)

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'predicted_score1', 'predicted_score2', 'prediction_time')
    list_filter = ('user', 'game',)
    search_fields = ('user__username', 'game__team1', 'game__team2')