# in knockout/admin.py

from django.contrib import admin
from .models import KnockoutGame, Prediction

@admin.register(KnockoutGame)
class KnockoutGameAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'stage', 'game_date', 'game_identifier', 'actual_winner')
    list_filter = ('stage', 'game_date')
    search_fields = ('team1', 'team2')
    actions = ['calculate_scores']

    def calculate_scores(self, request, queryset):
        for game in queryset:
            if game.actual_winner:
                predictions = Prediction.objects.filter(game__game_identifier=game.game_identifier)
                for prediction in predictions:
                    if prediction.predicted_winner == game.actual_winner:
                        prediction.score = 1  # Assign points as per your scoring logic
                    else:
                        prediction.score = 0
                    prediction.save()
        self.message_user(request, "Scores calculated based on actual winners.")
    calculate_scores.short_description = "Calculate scores for selected games"

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'predicted_winner', 'prediction_time', 'score')
    list_filter = ('user', 'game', 'predicted_winner')
    search_fields = ('user__username', 'game__team1', 'game__team2')
