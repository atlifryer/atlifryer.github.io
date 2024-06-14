from django.db import models
from django.conf import settings


class Game(models.Model):
    team1 = models.CharField(max_length=100, verbose_name="Team 1 Name")
    team2 = models.CharField(max_length=100, verbose_name="Team 2 Name")
    game_date = models.DateTimeField(verbose_name="Start Time")

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.game_date.strftime('%Y-%m-%d %H:%M')}"


class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    predicted_score1 = models.IntegerField()
    predicted_score2 = models.IntegerField()
    prediction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game}"
