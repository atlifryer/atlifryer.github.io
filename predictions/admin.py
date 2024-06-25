# predictions/admin.py
from django.contrib import admin
from .models import Game, Prediction, Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code', 'group')
    search_fields = ('name', 'country_code')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'game_date', 'actual_score1', 'actual_score2')
    list_filter = ('game_date',)
    search_fields = ('team1__name', 'team2__name')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'predicted_score1', 'predicted_score2', 'prediction_time')
    list_filter = ('user', 'game')
    search_fields = ('user__username', 'game__team1__name', 'game__team2__name')
