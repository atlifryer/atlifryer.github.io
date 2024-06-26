# predictions/models.py

from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Team Name")
    seed = models.IntegerField(null=True, blank=True, verbose_name="Seed Number")

    def __str__(self):
        return f"{self.name} (seed {self.seed})"


class Game(models.Model):
    team1 = models.CharField(max_length=100, verbose_name="Team 1 Name")
    team2 = models.CharField(max_length=100, verbose_name="Team 2 Name")
    game_date = models.DateTimeField(verbose_name="Start Time")
    actual_score1 = models.IntegerField(null=True, blank=True, verbose_name="Team 1 Actual Score")
    actual_score2 = models.IntegerField(null=True, blank=True, verbose_name="Team 2 Actual Score")

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.game_date.strftime('%Y-%m-%d %H:%M')}"


class KnockoutRound(models.Model):
    ROUND_CHOICES = [
        ('R16', '16 liða úrslit'),
        ('QF', '8 liða úrslit'),
        ('SF', 'Undanúrslit'),
        ('F', 'Úrslit'),
    ]
    round = models.CharField(max_length=3, choices=ROUND_CHOICES)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_round_display()} - {self.game} - {self.username}"


class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    predicted_score1 = models.IntegerField()
    predicted_score2 = models.IntegerField()
    prediction_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def calculate_score(self):
        if self.game.actual_score1 is None or self.game.actual_score2 is None:
            self.score = 0
            self.save()
            return  # No score calculation if game has not been scored yet

        points = 0
        result_actual = self.game.actual_score1 - self.game.actual_score2
        result_predicted = self.predicted_score1 - self.predicted_score2

        # Calculate points for correct result
        if (result_actual > 0 and result_predicted > 0) or (result_actual < 0 and result_predicted < 0) or (result_actual == result_predicted == 0):
            points += 3

        # Calculate points for correct goal difference
        if result_actual == result_predicted:
            points += 2

        # Calculate points for exact goals for each team
        if self.game.actual_score1 == self.predicted_score1:
            points += 1
        if self.game.actual_score2 == self.predicted_score2:
            points += 1

        self.score = points
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.game} Score: {self.score}"