# knockout/urls.py

from django.urls import path
from .views import PredictView

app_name = 'knockout'

urlpatterns = [
    path('predict/<stage>/', PredictView.as_view(), name='predict_stage'),
]
