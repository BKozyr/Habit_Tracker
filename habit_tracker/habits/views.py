from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from .forms import HabitForm, HabitRecordForm
from .models import Habit, HabitRecord


# Create your views here.

# def habit_list(request):
#     habits = Habit.objects.all()
#
#     return render(request,
#                   'habits/list.html',
#                   {'habits': habits})
#
# def habit_detail(request, slug):
#     habit = get_object_or_404(Habit, slug=slug)
#
#     return render(request,
#                   'habits/detail.html',
#                   {'habit': habit})

# class HabitListView(ListView):
#     queryset = Habit.objects.all()
#     context_object_name = "habits"
#     template_name = 'habits/list.html'

@login_required
def habit_list(request):
    date_str = request.GET.get('date')

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    prev_date = selected_date -timedelta(days=1)
    next_date = selected_date + timedelta(days=1)

    habits = Habit.objects.filter(user = request.user)
    total_habits = habits.count()
    habit_data = []
    for habit in habits:
        habit_data.append({
            'habit': habit,
            'total_done': habit.get_current_progress(selected_date)
        })

    context = {
        'habit_data': habit_data,
        'total_habits': total_habits,
        'selected_date': selected_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'today': date.today(),
    }

    return render(request, 'habits/list.html', context)
# class HabitDetailView(DetailView):
#     model = Habit
#     context_object_name = "habit"
#     template_name = 'habits/detail.html'

@login_required
def habit_detail(request, slug):
    habit = get_object_or_404(Habit, slug=slug, user = request.user)
    if request.method == 'POST':
        form = HabitRecordForm(request.POST)
        if form.is_valid():
            record_date = form.cleaned_data['date']
            record_amount = form.cleaned_data['amount_done']
            existing_record = HabitRecord.objects.filter(habit=habit, date=record_date).first()

            if record_amount == 0:
                if existing_record:
                    existing_record.delete()
            elif existing_record:
                existing_record.amount_done = record_amount
                existing_record.date = record_date
                existing_record.save()
            else:
                new_record = form.save(commit=False)
                new_record.habit = habit
                new_record.save()

            return redirect('habits:habit_detail' , slug = habit.slug)
    else:
        form = HabitRecordForm(initial={'date': date.today()})

    return render(request, 'habits/detail.html', {
        'habit' : habit,
        'form' : form
    })
@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)

            habit.user = request.user
            habit.slug = slugify(habit.name)

            habit.save()
            return redirect('habits:habit_list')
    else:
        form = HabitForm()

    return render(request, template_name='habits/form.html', context={'form': form})

@login_required
def habit_edit(request, slug):
    habit = get_object_or_404(Habit, slug=slug, user = request.user)

    if request.method == 'POST':
        form = HabitForm(request.POST,instance=habit)
        if form.is_valid():
            habit = form.save(commit=False)

            habit.user = request.user
            habit.slug = slugify(habit.name)

            habit.save()
            return redirect('habits:habit_detail',slug=habit.slug)
    else:
        form = HabitForm(instance=habit)

    return render(request, template_name='habits/form.html', context={'form': form})

@login_required
def habit_delete(request, slug):
    habit = get_object_or_404(Habit, slug=slug, user = request.user)

    if request.method == 'POST':
        habit.delete()
        return redirect('habits:habit_list')

    return render(request, 'habits/confirm_delete.html', {'habit': habit})

@login_required
def habit_quick_complete(request, pk):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, pk=pk, user = request.user)
        date_str = request.POST.get('date')
        if date_str:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            selected_date = date.today()

        record, created = HabitRecord.objects.get_or_create(
            habit=habit,
            date=selected_date,
            defaults={'amount_done': habit.target_amount}
        )

        if not created and record.amount_done < habit.target_amount:
            record.amount_done = habit.target_amount
            record.save()

        return redirect(f"/?date={selected_date.strftime('%Y-%m-%d')}")
    return redirect('habits:habit_list')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

