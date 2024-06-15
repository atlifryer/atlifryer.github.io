from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Game, Prediction
from .admin import calculate_scores
from django.utils import timezone

class ScoreCalculationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.game = Game.objects.create(
            team1='Germany', 
            team2='Scotland', 
            game_date=timezone.make_aware(timezone.datetime.now() + timezone.timedelta(days=1)),
            actual_score1=5, 
            actual_score2=1
        )
        self.prediction = Prediction.objects.create(
            user=self.user,
            game=self.game,
            predicted_score1=3,
            predicted_score2=1,
            prediction_time=timezone.now()
        )

    def test_correct_result_prediction(self):
        calculate_scores(None, None, Game.objects.filter(id=self.game.id))
        self.prediction.refresh_from_db()
        self.assertEqual(self.prediction.score, 4)

    def test_exact_score_prediction(self):
        self.prediction.predicted_score1 = 5
        self.prediction.save()
        calculate_scores(None, None, Game.objects.filter(id=self.game.id))
        self.prediction.refresh_from_db()
        self.assertEqual(self.prediction.score, 7)

    def test_incorrect_prediction(self):
        self.prediction.predicted_score1 = 1
        self.prediction.predicted_score2 = 2
        self.prediction.save()
        calculate_scores(None, None, Game.objects.filter(id=self.game.id))
        self.prediction.refresh_from_db()
        self.assertEqual(self.prediction.score, 0)