# predictions/migrations/0004_alter_game_actual_score1_alter_game_actual_score2.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("predictions", "0003_game_actual_score1_game_actual_score2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="actual_score1",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Team 1 Actual Score"
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="actual_score2",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Team 2 Actual Score"
            ),
        ),
    ]
