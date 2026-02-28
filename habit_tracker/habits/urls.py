from django.urls import path, include
from rest_framework.decorators import api_view

from . import views
from . import api_views
from .views import register

app_name = 'habits'

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('register/', register, name='register'),
    path('api/', api_views.get_habits, name='habit_api'),
    path('api/heatmap/<slug:slug>/', api_views.get_heap_map_data, name='habit_api'),
    path('create/', views.habit_create, name='habit_create'),
    path('<slug:slug>/', views.habit_detail, name='habit_detail'),
    path('<slug:slug>/edit/', views.habit_edit, name='habit_edit'),
    path('<slug:slug>/delete/', views.habit_delete, name='habit_delete'),
    path('<int:pk>/quick-complete/', views.habit_quick_complete, name='habit_quick_complete'),
]