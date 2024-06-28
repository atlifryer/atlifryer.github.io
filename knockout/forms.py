# knockout/forms.py

from django import forms
from .models import KnockoutGame

class PredictionForm(forms.Form):
    def __init__(self, games, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)
        for game in games:
            self.fields[f'game_{game.id}'] = forms.ChoiceField(
                choices=[
                    (game.team1, game.team1),
                    (game.team2, game.team2)
                ],
                label=f"{game.team1} — {game.team2}"
            )