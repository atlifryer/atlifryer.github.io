# predictions/models.py

from django.db import models
from .models import User
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Team Name")
    country_code = models.CharField(max_length=3, verbose_name="Country Code")
    group = models.CharField(max_length=10, verbose_name="Group")
    seed = models.IntegerField(null=True, blank=True, verbose_name="Seed Number")

    def __str__(self):
        return f"{self.name} ({self.country_code}, seed {self.seed})"


class KnockoutGame(models.Model):
    team1 = models.ForeignKey(Team, related_name='knockout_team1', on_delete=models.CASCADE, null=True, blank=True)
    team2 = models.ForeignKey(Team, related_name='knockout_team2', on_delete=models.CASCADE, null=True, blank=True)
    game_date = models.DateTimeField(verbose_name="Start Time")
    round = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="knockout_games")
    actual_score1 = models.IntegerField(null=True, blank=True, verbose_name="Team 1 Actual Score")
    actual_score2 = models.IntegerField(null=True, blank=True, verbose_name="Team 2 Actual Score")
    next_game = models.ForeignKey('self', related_name='previous_games', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.team1.name if self.team1 else 'TBD'} vs {self.team2.name if self.team2 else 'TBD'} on {self.game_date.strftime('%Y-%m-%d %H:%M')}"

    def update_next_game(self):
        if self.actual_score1 is not None and self.actual_score2 is not None:
            winner = self.team1 if self.actual_score1 > self.actual_score2 else self.team2
            if self.next_game:
                if self.next_game.team1 is None:
                    self.next_game.team1 = winner
                else:
                    self.next_game.team2 = winner
                self.next_game.save()


class Game(models.Model):
    team1 = models.CharField(max_length=100, verbose_name="Team 1 Name")
    team2 = models.CharField(max_length=100, verbose_name="Team 2 Name")
    team1_group = models.CharField(max_length=10, verbose_name="Team 1 Group", default="X", blank=True)
    team2_group = models.CharField(max_length=10, verbose_name="Team 2 Group", default="X", blank=True)
    team1_country_code = models.CharField(max_length=3, verbose_name="Team 1 Country Code", default="IS", blank=True)
    team2_country_code = models.CharField(max_length=3, verbose_name="Team 2 Country Code", default="IS", blank=True)
    game_date = models.DateTimeField(verbose_name="Start Time")
    actual_score1 = models.IntegerField(null=True, blank=True, verbose_name="Team 1 Actual Score")
    actual_score2 = models.IntegerField(null=True, blank=True, verbose_name="Team 2 Actual Score")

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.game_date.strftime('%Y-%m-%d %H:%M')}"


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
        round = models.IntegerField(default=1)
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
    

class KnockoutPrediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(KnockoutGame, on_delete=models.CASCADE)
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