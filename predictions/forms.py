# predictions/forms.py

from django import forms
from .models import Prediction, Game

class PredictionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        games = kwargs.pop('games', None)
        super(PredictionForm, self).__init__(*args, **kwargs)
        if games:
            for game in games:
                self.fields[f'predicted_score1_{game.id}'] = forms.IntegerField(label=f'{game.team1} Score', min_value=0)
                self.fields[f'predicted_score2_{game.id}'] = forms.IntegerField(label=f'{game.team2} Score', min_value=0)
