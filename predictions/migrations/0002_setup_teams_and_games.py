# predictions/migrations/0002_setup_teams_and_games.py

from django.db import migrations, models
import datetime

def add_team_and_games(apps, schema_editor):
    Team = apps.get_model('predictions', 'Team')
    Game = apps.get_model('predictions', 'Game')

    # Define the teams and their seeds
    team_data = [
        ('Spánn', 1),
        ('Georgía', 2),
        ('Þýskaland', 3),
        ('Danmörk', 4),
        ('Portúgal', 5),
        ('Slóvenía', 6),
        ('Frakkland', 7),
        ('Belgía', 8),
        ('Rúmenía', 9),
        ('Holland', 10),
        ('Austurríki', 11),
        ('Tyrkland', 12),
        ('England', 13),
        ('Slóvakía', 14),
        ('Sviss', 15),
        ('Ítalía', 16)
    ]
    teams = {}
    for name, seed in team_data:
        team = Team.objects.create(name=name, seed=seed)
        teams[seed] = team

    # Define the games based on seeds
    games_data = [
        (1, 2, datetime.datetime(2024, 6, 30, 19, 0)),
        (3, 4, datetime.datetime(2024, 6, 29, 19, 0)),
        (5, 6, datetime.datetime(2024, 7, 1, 19, 0)),
        (7, 8, datetime.datetime(2024, 7, 1, 16, 0)),
        (9, 10, datetime.datetime(2024, 7, 2, 16, 0)),
        (11, 12, datetime.datetime(2024, 7, 2, 19, 0)),
        (13, 14, datetime.datetime(2024, 6, 30, 16, 0)),
        (15, 16, datetime.datetime(2024, 6, 29, 16, 0))
    ]
    for team1_seed, team2_seed, game_date in games_data:
        Game.objects.create(team1=teams[team1_seed].name, team2=teams[team2_seed].name, game_date=game_date)

class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),  # Adjust the dependency to your last applied migration if necessary
    ]

    operations = [
        migrations.RunPython(add_team_and_games),
    ]
