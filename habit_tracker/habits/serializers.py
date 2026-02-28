from datetime import date

from rest_framework import serializers
from .models import Habit, HabitRecord


class HabitSerializer(serializers.ModelSerializer):
    current_progress = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'name', 'target_amount', 'current_progress', 'streak']

    def get_current_progress(self, obj):
        return obj.get_current_progress(date.today())

    def get_streak(self, obj):
        return obj.get_streak()
