# gym/forms.py

from django import forms
from .models import Workout, Exercise

class WorkoutForm(forms.ModelForm):
    workout_day = forms.ChoiceField(choices=Exercise.WORKOUT_TYPE_CHOICES)
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.none())

    class Meta:
        model = Workout
        fields = ['workout_day', 'exercise', 'weight', 'unit', 'reps', 'sets']
        widgets = {
            'unit': forms.Select(choices=[('kg', 'kg'), ('lbs', 'lbs')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['workout_day'].initial = Exercise.CHEST_SHOULDERS_TRICEPS
        if 'workout_day' in self.data:
            workout_day = self.data.get('workout_day')
            self.fields['exercise'].queryset = Exercise.objects.filter(workout_type=workout_day)
        elif self.instance.pk:
            self.fields['exercise'].queryset = self.instance.exercise.workout_day.exercise_set
        else:
            self.fields['exercise'].queryset = Exercise.objects.filter(workout_type=self.fields['workout_day'].initial)
