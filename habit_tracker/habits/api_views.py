from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Habit, HabitRecord
from .serializers import HabitSerializer
@api_view(['GET'])
def get_habits(request):
    habits = Habit.objects.all()
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_heap_map_data(request, slug):
    records = HabitRecord.objects.filter(
        habit__user=request.user,
        habit__slug = slug,
    )

    daily_stats = records.values('date').annotate(value=Sum('amount_done')).order_by('date')

    return Response(list(daily_stats))
