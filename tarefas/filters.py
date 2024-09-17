import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    date_range = django_filters.DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Task
        fields = ['title', 'date_range']
