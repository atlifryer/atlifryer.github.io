# in knockout/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import KnockoutGame

@receiver(post_save, sender=KnockoutGame)
def propagate_actual_winner(sender, instance, **kwargs):
    if instance.actual_winner:
        KnockoutGame.objects.filter(game_identifier=instance.game_identifier).update(actual_winner=instance.actual_winner)
