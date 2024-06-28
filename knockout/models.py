# in knockout/models.py

from django.db import models
from django.conf import settings


class KnockoutGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='knockout_games', null=True, blank=True)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    stage = models.CharField(max_length=50)
    game_date = models.DateTimeField()
    game_identifier = models.CharField(max_length=20)  # Unique identifier like 'r16_1', 'qf_1', etc.
    actual_winner = models.CharField(max_length=100, null=True, blank=True)  # Field to store the actual winner

    def __str__(self):
        return f"{self.team1} vs {self.team2} ({self.stage})"


class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='knockout_predictions')
    game = models.ForeignKey(KnockoutGame, on_delete=models.CASCADE)
    predicted_winner = models.CharField(max_length=100)
    prediction_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)  # Field to store the score

    def __str__(self):
        return f"{self.user.username} - {self.game} - {self.predicted_winner}"
