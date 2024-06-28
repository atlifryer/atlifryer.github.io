# knockouts/urls.py

from django.urls import path
from .views import tournament_view

urlpatterns = [
    path('<str:round_name>/', tournament_view, name='tournament'),
]
