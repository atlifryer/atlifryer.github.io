# predictions/migrations/0005_alter_prediction_score.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("predictions", "0004_alter_game_actual_score1_alter_game_actual_score2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prediction", name="score", field=models.IntegerField(default=0),
        ),
    ]
