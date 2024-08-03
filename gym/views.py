# gym/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.dateformat import format
from .forms import WorkoutForm
from .models import Exercise, Workout
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Max, Q

@staff_member_required
def last_workout_details(request):
    exercise_id = request.GET.get('exercise_id')
    if not exercise_id:
        return JsonResponse({'error': 'No exercise specified'}, status=400)

    today = timezone.localdate()

    latest_date = Workout.objects.filter(
        exercise_id=exercise_id,
        date_time__date__lt=today
    ).aggregate(Max('date_time'))['date_time__max']

    if not latest_date:
        return JsonResponse({'error': 'No workouts found for this exercise'}, status=404)

    workouts = Workout.objects.filter(
        exercise_id=exercise_id, 
        date_time__date=latest_date.date()
    ).order_by('date_time')

    last_workout_day = format(timezone.localtime(latest_date), 'l, F jS')
    workouts_data = [{
        'reps': workout.reps,
        'weight': workout.weight,
        'unit': workout.unit,
        'sets': workout.sets,
    } for workout in workouts]

    return JsonResponse({'date': last_workout_day, 'workouts': workouts_data})


@staff_member_required
def load_exercises(request):
    workout_day = request.GET.get('workout_day')
    exercises = Exercise.objects.filter(workout_type=workout_day).order_by('name')
    return render(request, 'gym/exercise_dropdown_list_options.html', {'exercises': exercises})

@staff_member_required
def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.date_time = timezone.now()  # Set the current time at the moment of saving
            workout.save()
            # Reinitialize the form for subsequent entries with some fields preserved
            data = {
                'workout_day': form.cleaned_data['workout_day'],
                'exercise': form.cleaned_data['exercise'],
                'unit': form.cleaned_data['unit'],
            }
            form = WorkoutForm(initial=data)  # Initialize form with specific fields preserved
    else:
        form = WorkoutForm()
    return render(request, 'gym/add_workout.html', {'form': form})
