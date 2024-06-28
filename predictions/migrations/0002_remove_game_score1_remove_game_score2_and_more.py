# predictions/migrations/0002_remove_game_score1_remove_game_score2_and_more.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("predictions", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="game", name="score1",),
        migrations.RemoveField(model_name="game", name="score2",),
        migrations.AlterField(
            model_name="game",
            name="game_date",
            field=models.DateTimeField(verbose_name="Start Time"),
        ),
        migrations.AlterField(
            model_name="game",
            name="team1",
            field=models.CharField(max_length=100, verbose_name="Team 1 Name"),
        ),
        migrations.AlterField(
            model_name="game",
            name="team2",
            field=models.CharField(max_length=100, verbose_name="Team 2 Name"),
        ),
    ]
