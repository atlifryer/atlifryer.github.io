# in knockout/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import PredictionForm
from .models import KnockoutGame, Prediction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta

class PredictView(LoginRequiredMixin, View):
    def get(self, request, stage):
        if stage != 'R16':
            # Check if user has any games for the current stage
            if not KnockoutGame.objects.filter(stage=stage, user=request.user).exists():
                # Redirect to the previous stage if no games found for current stage
                previous_stage = self.get_previous_stage(stage)
                if previous_stage:
                    return redirect('knockout:predict_stage', stage=previous_stage)
        
        if stage == 'R16':
            games = KnockoutGame.objects.filter(stage=stage)
        else:
            games = KnockoutGame.objects.filter(stage=stage, user=request.user)
        
        form = PredictionForm(games)
        return render(request, 'knockout/stage_prediction_form.html', {'form': form, 'stage': stage})

    def post(self, request, stage):
        if stage == 'R16':
            games = KnockoutGame.objects.filter(stage=stage)
        else:
            games = KnockoutGame.objects.filter(stage=stage, user=request.user)
        
        form = PredictionForm(games, request.POST)
        if form.is_valid():
            # Block predictions if the first game has started
            first_game = games.order_by('game_date').first()
            if first_game and first_game.game_date <= timezone.now():
                return render(request, 'knockout/stage_prediction_form.html', {
                    'form': form,
                    'error': 'Predictions are closed as the first game has started.'
                })

            # Save each prediction
            for game in games:
                predicted_winner = form.cleaned_data[f'game_{game.id}']
                Prediction.objects.update_or_create(
                    user=request.user,
                    game=game,
                    defaults={'predicted_winner': predicted_winner}
                )

            # Determine next stage and delete old games
            if stage == 'R16':
                self.delete_old_games('QF')
                self.create_next_round_games(form.cleaned_data, 'QF', request.user)
                next_stage = 'QF'
            elif stage == 'QF':
                self.delete_old_games('SF')
                self.create_next_round_games(form.cleaned_data, 'SF', request.user)
                next_stage = 'SF'
            elif stage == 'SF':
                self.delete_old_games('F')
                self.create_next_round_games(form.cleaned_data, 'F', request.user)
                next_stage = 'F'
            elif stage == 'F':
                # Get the winner's prediction and render the splash page
                winner = list(form.cleaned_data.values())[0]
                return render(request, 'knockout/winner_splash.html', {'winner': winner})

            return redirect('knockout:predict_stage', stage=next_stage)
        return render(request, 'knockout/stage_prediction_form.html', {'form': form, 'stage': stage})

    def delete_old_games(self, next_stage):
        KnockoutGame.objects.filter(stage=next_stage, user=self.request.user).delete()

    def create_next_round_games(self, predictions, next_stage, user):
        new_games = []
        next_stage_dates = {
            'QF': timezone.now() + timedelta(days=7),  # Example date for QF
            'SF': timezone.now() + timedelta(days=14),  # Example date for SF
            'F': timezone.now() + timedelta(days=21),  # Example date for Final
        }
        game_identifiers = {
            'QF': ['qf_1', 'qf_2', 'qf_3', 'qf_4'],
            'SF': ['sf_1', 'sf_2'],
            'F': ['f_1'],
        }

        if next_stage in ['QF', 'SF']:
            winning_teams = list(predictions.values())
            for i in range(0, len(winning_teams), 2):
                team1 = winning_teams[i]
                team2 = winning_teams[i + 1]
                game_id = game_identifiers[next_stage][i // 2]
                new_games.append((team1, team2, game_id))
        elif next_stage == 'F':
            winning_teams = list(predictions.values())
            if len(winning_teams) == 2:
                team1 = winning_teams[0]
                team2 = winning_teams[1]
                game_id = game_identifiers[next_stage][0]
                new_games.append((team1, team2, game_id))

        for team1, team2, game_id in new_games:
            KnockoutGame.objects.create(user=user, team1=team1, team2=team2, stage=next_stage, game_date=next_stage_dates[next_stage], game_identifier=game_id)

    def get_previous_stage(self, current_stage):
        stages = ['R16', 'QF', 'SF', 'F']
        current_index = stages.index(current_stage)
        if current_index > 0:
            return stages[current_index - 1]
        return None
