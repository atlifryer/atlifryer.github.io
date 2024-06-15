# predictions/views.py

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from .models import Game, Prediction
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'predictions/game_list.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.all().order_by('game_date')

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
        predictions = Prediction.objects.filter(
            user=self.request.user,
            game__in=context['games']
        ).select_related('game')
        
        # Calculate the score for each prediction on the fly
        for prediction in predictions:
            prediction.calculate_score()  # Ensure the score is calculated

        context['predictions'] = {prediction.game.id: prediction for prediction in predictions}
        context['now'] = timezone.now()
        return context


class LeaderboardView(LoginRequiredMixin, ListView):
    model = User
    template_name = "predictions/leaderboard.html"
    context_object_name = "leaderboard_users"

    def get_queryset(self):
        return User.objects.annotate(total_score=Sum('prediction__score')).order_by('-total_score')
