# Generated by Django 5.0 on 2024-06-14 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("predictions", "0002_remove_game_score1_remove_game_score2_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="actual_score1",
            field=models.IntegerField(default=0, verbose_name="Team 1 Actual Score"),
        ),
        migrations.AddField(
            model_name="game",
            name="actual_score2",
            field=models.IntegerField(default=0, verbose_name="Team 2 Actual Score"),
        ),
        migrations.AddField(
            model_name="prediction",
            name="score",
            field=models.IntegerField(default=0, verbose_name="Score"),
        ),
    ]