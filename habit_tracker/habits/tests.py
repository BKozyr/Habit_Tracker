from django.contrib.auth.models import User
from django.test import TestCase
from datetime import date, timedelta
from .models import Habit, HabitRecord


# Create your tests here.

class HabitModelTesty(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            username = 'testuser',
            password = 'testpassword123'
        )

        self.test_habit = Habit.objects.create(
            name="Bieganie",
            slug = "beiganie",
            user = self.test_user
        )

    def test_habit_default_target_amount(self):
        self.assertEqual(1, self.test_habit.target_amount)

    def test_habit_str_func(self):
        self.assertEqual(str(self.test_habit), "Bieganie")

    def test_current_progress(self):
        for i in range(5):
            self.test_record = HabitRecord.objects.create(
                habit = self.test_habit,
                date = date.today() - timedelta(days=i),
                amount_done = 1
            )

        self.assertEqual(self.test_habit.get_current_progress(),1)
        self.assertEqual(self.test_habit.get_current_progress(date.today() - timedelta(days=10)), 0)


    def test_get_streak(self):
        for i in range(5):
            self.test_record = HabitRecord.objects.create(
                habit = self.test_habit,
                date = date.today() - timedelta(days=i),
                amount_done = 1
            )

        self.assertEqual(self.test_habit.get_streak(),5)

    def test_get_streak_break_streak(self):
        for i in range(2,5):
            self.test_record = HabitRecord.objects.create(
                habit = self.test_habit,
                date = date.today() - timedelta(days=i),
                amount_done = 1
            )

        self.assertEqual(self.test_habit.get_streak(),0)

    def test_get_streak_not_done_yet(self):
        for i in range(1, 5):
            self.test_record = HabitRecord.objects.create(
                habit=self.test_habit,
                date=date.today() - timedelta(days=i),
                amount_done=1
            )

        self.assertEqual(self.test_habit.get_streak(), 4)
