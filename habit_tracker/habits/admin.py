from django.contrib import admin
from .models import Habit, HabitRecord

# Register your models here.


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'frequency']
    list_filter = ['frequency', 'created_at']  # To doda pasek filtrów po prawej stronie
    search_fields = ['name', 'description']  # To doda pasek wyszukiwania na górze
    prepopulated_fields = {'slug': ('name',)}  # Automatyczny slug

@admin.register(HabitRecord)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'amount_done']
    list_filter = ['habit', 'date']  # To doda pasek filtrów po prawej stronie
