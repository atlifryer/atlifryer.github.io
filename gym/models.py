# gym/models.py

from django.db import models

class Exercise(models.Model):
    LEG_DAY = 'Leg Day'
    CHEST_SHOULDERS_TRICEPS = 'Chest/Shoulders/Triceps'
    BACK_BICEPS = 'Back/Biceps'
    CORE_OTHER = 'Core/Other'
    WORKOUT_TYPE_CHOICES = [
        (LEG_DAY, 'Leg Day'),
        (CHEST_SHOULDERS_TRICEPS, 'Chest/Shoulders/Triceps'),
        (BACK_BICEPS, 'Back/Biceps'),
        (CORE_OTHER, 'Core/Other'),
    ]

    name = models.CharField(max_length=100)
    workout_type = models.CharField(
        max_length=50,
        choices=WORKOUT_TYPE_CHOICES,
        default=CORE_OTHER,
    )
    primary_muscle = models.CharField(max_length=100)
    secondary_muscle = models.CharField(max_length=100, blank=True)
    additional_muscles = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    date_time = models.DateTimeField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.FloatField()
    unit = models.CharField(max_length=10)
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):
        return f'{self.exercise.name} on {self.date_time}'
