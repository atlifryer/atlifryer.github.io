# gym/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add_workout/', views.add_workout, name='add_workout'),
    path('ajax/load-exercises/', views.load_exercises, name='ajax_load_exercises'),  # AJAX URL for loading exercises
    path('ajax/last-workout/', views.last_workout_details, name='last_workout_details'), # AJAX URL for last workout details
]
