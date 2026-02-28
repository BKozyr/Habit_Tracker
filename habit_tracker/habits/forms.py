from django import forms
from .models import Habit, HabitRecord


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'frequency', 'description', 'target_amount', 'unit']

class HabitRecordForm(forms.ModelForm):
    class Meta:
        model = HabitRecord
        fields = ['amount_done', 'date']
        labels={
            'date': "Data",
            'amount_done': "Ile zrobiłeś?"
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }