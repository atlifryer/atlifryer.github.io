# predictions/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.conf import settings
from .models import Game, Prediction, KnockoutRound

def get_winner(game, user):
    prediction = Prediction.objects.get(game=game, user=user)
    if prediction.predicted_score1 > prediction.predicted_score2:
        return game.team1
    elif prediction.predicted_score1 < prediction.predicted_score2:
        return game.team2
    else:
        return None # Tie logic here later
    
def create_next_round_games(round_name, user, pairs, dates):
    for idx, (team1, team2) in enumerate(pairs):
        game_date = dates[idx]
        game = Game.objects.create(
            team1=team1,
            team2=team2,
            game_date=game_date
        )
        KnockoutRound.objects.create(round=round_name, game=game, user=user)

@receiver(post_save, sender=Game)
def update_scores(sender, instance, created, **kwargs):
    if instance.actual_score1 is not None and instance.actual_score2 is not None:
        predictions = Prediction.objects.filter(game=instance)
        for prediction in predictions:
            prediction.calculate_score()

@receiver(post_save, sender=Prediction)
def create_next_round_matches(sender, instance, **kwargs):
    user = instance.user
    knockout_rounds = instance.game.knockoutround_set.filter(user=user)
    if not knockout_rounds.exists():
        return
    
    round = knockout_rounds.first().round

    if round == 'R16':
        games = Game.objects.filter(knockoutround__round='R16', knockoutround__user=user)
        winners = [get_winner(game, user) for game in games]
        pairs = list(zip(winners[::2], winners[1::2]))  # Create pairs for quarterfinals
        dates = [
            datetime(2024, 7, 5, 16, 0),
            datetime(2024, 7, 5, 19, 0),
            datetime(2024, 7, 6, 19, 0),
            datetime(2024, 7, 6, 16, 0),
        ]
        create_next_round_games('QF', user, pairs, dates)

    elif round == 'QF':
        games = Game.objects.filter(knockoutround__round='QF', knockoutround__user=user)
        winners = [get_winner(game, user) for game in games]
        pairs = list(zip(winners[::2], winners[1::2]))  # Create pairs for semifinals
        dates = [
            datetime(2024, 7, 9, 19, 0),
            datetime(2024, 7, 10, 19, 0),
        ]
        create_next_round_games('SF', user, pairs, dates)

    elif round == 'SF':
        games = Game.objects.filter(knockoutround__round='SF', knockoutround__user=user)
        winners = [get_winner(game, user) for game in games]
        if len(winners) == 2:
            dates = [datetime(2024, 7, 14, 19, 0)]
            create_next_round_games('F', user, [(winners[0], winners[1])], dates)