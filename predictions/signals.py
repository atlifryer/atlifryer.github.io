# predictions/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Prediction

@receiver(post_save, sender=Game)
def update_scores(sender, instance, created, **kwargs):
    if instance.actual_score1 is not None and instance.actual_score2 is not None:
        predictions = Prediction.objects.filter(game=instance)
        for prediction in predictions:
            prediction.calculate_score()