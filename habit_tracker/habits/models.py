from collections import defaultdict
from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.

class Habit(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "D", "Daily"
        WEEKLY = "W", "Weekly"
        MONTHLY = "M", "Monthly"
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=1,
        choices=Frequency.choices,
        default=Frequency.DAILY
    )
    target_amount = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=50, blank=True)

    def get_current_progress(self, target_date = date.today()):

        if self.frequency == self.Frequency.DAILY:
            records = self.records.filter(date=target_date)
        elif self.frequency == self.Frequency.WEEKLY:
            start_of_week = target_date - timedelta(days=target_date.weekday())
            records = self.records.filter(date__gte=start_of_week, date__lte=target_date)
        elif self.frequency == self.Frequency.MONTHLY:
            records = self.records.filter(date__year=target_date.year, date__month=target_date.month)
        else:
            records = self.records.none()

        total = records.aggregate(Sum('amount_done'))['amount_done__sum']
        return total or 0

    def get_streak(self):
        today = date.today()
        streak=0

        totals = defaultdict(int)
        for record in self.records.all():
            if self.frequency == self.Frequency.DAILY:
                index = record.date
            if self.frequency == self.Frequency.WEEKLY:
                index = record.date - timedelta(days=record.date.weekday())
            if self.frequency == self.Frequency.MONTHLY:
                index = (record.date.year, record.date.month)

            totals[index] += record.amount_done

        completed_period = {i for i, total in totals.items() if total >= self.target_amount}

        if self.frequency == self.Frequency.DAILY:
            current_period = today
            step = lambda  d: d - timedelta(days=1)
        elif self.frequency == self.Frequency.WEEKLY:
            current_period = today - timedelta(days=today.weekday())
            step = lambda  d: d - timedelta(weeks=1)
        elif self.frequency == self.Frequency.MONTHLY:
            current_period = (today.year, today.month)
            def step(ym):
                y,m = ym
                return (y, m - 1) if m > 1 else (y-1,12)

        if current_period not in completed_period:
            current_period = step(current_period)

        while current_period in completed_period:
            streak +=1
            current_period = step(current_period)

        return streak if streak >= 3 else 0

    def __str__(self):
        return self.name

class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="records")
    date = models.DateField()
    amount_done = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']
        unique_together = ['habit', 'date']

    def __str__(self):
        return f"{self.habit.name} | {self.date} | Wykonano: {self.amount_done}"

