from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from .models import Game, Prediction


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
                print(f"Saved: {predicted_score1}-{predicted_score2} for game {game.id}")  # Debugging line
        return redirect('game_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch user's predictions
        user_predictions = {prediction.game.id: prediction for prediction in Prediction.objects.filter(user=self.request.user)}
        context['user_predictions'] = user_predictions
        # Add current time to the context
        context['now'] = timezone.now()
        return context


