# predictions/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Prediction, KnockoutGame, KnockoutPrediction

@receiver(post_save, sender=Game)
def update_scores(sender, instance, created, **kwargs):
    if instance.actual_score1 is not None and instance.actual_score2 is not None:
        predictions = Prediction.objects.filter(game=instance)
        for prediction in predictions:
            prediction.calculate_score()

@receiver(post_save, sender=KnockoutGame)
def update_knockout_scores_and_advance_winner(sender, instance, **kwargs):
    if instance.actual_score1 is not None and instance.actual_score2 is not None:
        knockout_predictions = KnockoutPrediction.objects.filter(game=instance)
        for prediction in knockout_predictions:
            prediction.calculate_score()
        instance.update_next_game()