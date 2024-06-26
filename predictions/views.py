# predictions/views.py

from django.views.generic import ListView, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime
from .models import Game, KnockoutGame, Prediction, KnockoutPrediction, Team
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncDay
from django.utils.timezone import now
from django.urls import reverse

User = get_user_model()

game_schedule = {
    'qf1': datetime(2024, 7, 5, 16, 0),  # Date and time for Quarter-final 1
    'qf2': datetime(2024, 7, 5, 19, 0),  # Date and time for Quarter-final 2
    'qf3': datetime(2024, 7, 6, 19, 0),  # Date and time for Quarter-final 3
    'qf4': datetime(2024, 7, 6, 16, 0),  # Date and time for Quarter-final 4
    'sf1': datetime(2024, 7, 9, 19, 0),  # Date and time for Semi-final 1
    'sf2': datetime(2024, 7, 10, 19, 0),  # Date and time for Semi-final 2
    'final': datetime(2024, 7, 14, 19, 0),  # Date and time for the Final
}

def create_placeholder_knockout_games():
    rounds = ['qf1', 'qf2', 'qf3', 'qf4', 'sf1', 'sf2', 'final']
    for round_key in rounds:
        KnockoutGame.objects.create(
            game_date=game_schedule[round_key],
            round=round_key[:2].upper()
        )
    print("Placeholder games for knockout rounds created.")

def update_knockout_games_with_teams():
    # Example seeds mapping, modify based on actual logic to determine winners
    seed_winners = {1: 'Team A', 2: 'Team B'}  # Update with real team retrieval logic

    for game in KnockoutGame.objects.filter(round='QF'):
        if game.name == 'qf1':
            game.team1_id = seed_winners.get(1)  # Assuming you have a mapping of seeds to team IDs
            game.team2_id = seed_winners.get(2)
            game.save()


class AdvanceRoundView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        current_round = kwargs.get('round_number')
        games = KnockoutGame.objects.filter(round=current_round)

        # Process each game's predictions
        for game in games:
            predicted_score1 = request.POST.get(f'predicted_score1_{game.id}')
            predicted_score2 = request.POST.get(f'predicted_score2_{game.id}')

            # Ensure both scores are provided
            if predicted_score1 is not None and predicted_score2 is not None:
                predicted_score1 = int(predicted_score1)
                predicted_score2 = int(predicted_score2)

                # Update or create predictions
                KnockoutPrediction.objects.update_or_create(
                    user=request.user,
                    game=game,
                    defaults={
                        'predicted_score1': predicted_score1,
                        'predicted_score2': predicted_score2
                    }
                )
            else:
                # Redirect back with an error message if predictions are missing
                return HttpResponseRedirect(reverse('knockout_game_list') + "?error=complete_all_predictions")

        # Advance to the next round
        return self.advance_to_next_round(current_round)

    def get(self, request, *args, **kwargs):
        current_round = kwargs.get('round_number')

        # Simply checks and advances rounds
        return self.advance_to_next_round(current_round)

    def advance_to_next_round(self, current_round, request):
        games = KnockoutGame.objects.filter(round=current_round)
        next_round_seeds = []

        # Check if all games have predictions and gather winners
        for game in games:
            if not KnockoutPrediction.objects.filter(game=game).exists():
                return HttpResponseRedirect(reverse('knockout_game_list') + "?error=complete_all_predictions")

            prediction = KnockoutPrediction.objects.get(game=game)
            winner = game.team1 if prediction.predicted_score1 > prediction.predicted_score2 else game.team2
            next_round_seeds.append(winner.seed)

        # Sort seeds and create games for the next round
        next_round_seeds.sort()

        next_round = 'sf1' if current_round == 'QF' else 'final'  # Simplify or expand logic as needed
        next_game_date = game_schedule[next_round]

        for i in range(0, len(next_round_seeds), 2):
            if i + 1 < len(next_round_seeds):
                team1 = Team.objects.get(seed=next_round_seeds[i])
                team2 = Team.objects.get(seed=next_round_seeds[i + 1])
                KnockoutGame.objects.create(
                    team1=team1,
                    team2=team2,
                    round=current_round + 1,
                    game_date=next_game_date,  # Use the correctly determined date
                    user=request.user
                )

        return HttpResponseRedirect(reverse('knockout_game_list'))
    

class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'predictions/game_list.html'
    context_object_name = 'games'

    def get_queryset(self):
        queryset = Game.objects.all().order_by('game_date')
        game_date_gte = self.request.GET.get('game_date__gte')
        
        if game_date_gte:
            queryset = queryset.filter(game_date__date__gte=game_date_gte)
        else:
            game_date = self.request.GET.get('game_date')
            if game_date:
                game_date = parse_date(game_date)
                queryset = queryset.filter(game_date__date=game_date)

        return queryset

    def post(self, request, *args, **kwargs):
        games = self.get_queryset()
        for game in games:
            predicted_score1 = request.POST.get(f'predicted_score1_{game.id}')
            predicted_score2 = request.POST.get(f'predicted_score2_{game.id}')
            if predicted_score1 and predicted_score2 and game.game_date > timezone.now():
                Prediction.objects.update_or_create(
                    user=request.user,
                    game=game,
                    defaults={
                        'predicted_score1': predicted_score1,
                        'predicted_score2': predicted_score2
                    }
                )
        return redirect('game_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_games = Game.objects.all()
        unique_dates = all_games.annotate(date=TruncDay('game_date')).order_by('date').values_list('date', flat=True).distinct()
        context['unique_dates'] = unique_dates
        
        filtered_games = self.get_queryset()
        context['games'] = filtered_games

        predictions = Prediction.objects.filter(
            user=self.request.user,
            game__in=filtered_games
        ).select_related('game')

        for prediction in predictions:
            prediction.calculate_score()
        
        context['predictions'] = {prediction.game.id: prediction for prediction in predictions}
        context['selected_date'] = self.request.GET.get('game_date', '')
        context['today'] = now().date()
        context['now'] = timezone.now()
        return context


class KnockoutGameListView(LoginRequiredMixin, ListView):
    model = KnockoutGame
    template_name = 'predictions/knockout_game_list.html'
    context_object_name = 'knockout_games'

    def get_queryset(self):
        queryset = KnockoutGame.objects.all().order_by('game_date')
        game_date_gte = self.request.GET.get('game_date__gte')
        
        if game_date_gte:
            queryset = queryset.filter(game_date__date__gte=game_date_gte)
        else:
            game_date = self.request.GET.get('game_date')
            if game_date:
                game_date = parse_date(game_date)
                queryset = queryset.filter(game_date__date=game_date)

        return queryset

    def post(self, request, *args, **kwargs):
        games = self.get_queryset()
        for game in games:
            predicted_score1 = request.POST.get(f'predicted_score1_{game.id}')
            predicted_score2 = request.POST.get(f'predicted_score2_{game.id}')
            if predicted_score1 and predicted_score2 and game.game_date > timezone.now():
                KnockoutPrediction.objects.update_or_create(
                    user=request.user,
                    game=game,
                    defaults={
                        'predicted_score1': predicted_score1,
                        'predicted_score2': predicted_score2
                    }
                )
        return redirect('knockout_game_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_round = self.kwargs.get('round_number') or self.request.GET.get('round_number') or 1
        context['current_round'] = current_round
        context['next_round_url'] = reverse('advance_round', kwargs={'round_number': current_round})
        
        all_games = KnockoutGame.objects.all()
        unique_dates = all_games.annotate(date=TruncDay('game_date')).order_by('date').values_list('date', flat=True).distinct()
        context['unique_dates'] = unique_dates
        
        filtered_games = self.get_queryset()
        context['knockout_games'] = filtered_games

        predictions = KnockoutPrediction.objects.filter(
            user=self.request.user,
            game__in=filtered_games
        ).select_related('game')

        for prediction in predictions:
            prediction.calculate_score()
        
        context['knockout_predictions'] = {prediction.game.id: prediction for prediction in predictions}
        context['selected_date'] = self.request.GET.get('game_date', '')
        context['today'] = now().date()
        context['now'] = timezone.now()
        return context
    

class LeaderboardView(LoginRequiredMixin, ListView):
    model = User
    template_name = "predictions/leaderboard.html"
    context_object_name = "leaderboard_users"

    def get_queryset(self):
        return User.objects.annotate(total_score=Sum('prediction__score')).filter(total_score__gte=0).order_by('-total_score')