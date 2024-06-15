# predictions/admin.py

from django.contrib import admin
from .models import Game, Prediction

@admin.action(description='Recalculate scores for selected games')
def recalculate_scores(modeladmin, request, queryset):
    for game in queryset:
        predictions = Prediction.objects.filter(game=game)
        for prediction in predictions:
            prediction.calculate_score()


class GameAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'game_date', 'actual_score1', 'actual_score2')
    list_filter = ('game_date',)
    search_fields = ('team1', 'team2',)
    actions = [recalculate_scores]


class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'predicted_score1', 'predicted_score2', 'prediction_time')
    list_filter = ('user', 'game',)
    search_fields = ('user__username', 'game__team1', 'game__team2')

admin.site.register(Game, GameAdmin)
admin.site.register(Prediction)