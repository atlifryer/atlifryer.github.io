import csv
from django.core.management.base import BaseCommand
from gym.models import Exercise, Workout
from django.utils.dateparse import parse_datetime
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads data from CSV files into the database'

    def handle(self, *args, **options):
        # Importing Exercises
        with open('gym/data/muscles.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Exercise.objects.get_or_create(
                    name=row['Exercise'],
                    defaults={
                        'workout_type': row['Exercise day'],
                        'primary_muscle': row['Primary Muscle'],
                        'secondary_muscle': row['Secondary Muscle'] or '',
                        'additional_muscles': row['Additional Muscles'] or ''
                    }
                )

        # Importing Workouts
        with open('gym/data/workouts.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                exercise = Exercise.objects.get(name=row['Exercise'])
                date_str = row['Date'] + ' 12:00:00'  # Append a default time
                date_time = datetime.strptime(date_str, '%B %d, %Y %H:%M:%S')  # Adjust the format string as needed
                Workout.objects.create(
                    date_time=date_time,
                    exercise=exercise,
                    weight=float(row['Weight']),
                    unit=row['Unit'],
                    reps=int(row['Reps']),
                    sets=int(row['Sets'])
                )
