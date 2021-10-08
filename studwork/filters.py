import django_filters
from django.forms.widgets import ChoiceWidget
from django_filters import RangeFilter, CharFilter, OrderingFilter
from django_filters.widgets import BooleanWidget, RangeWidget

from .models import Student


class StudentFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    age = RangeFilter(field_name='age', lookup_expr='exact', widget = RangeWidget())
    o = OrderingFilter(fields={'id': 'id'}, empty_label = None, label ="Сортировка")

    class Meta:
        model = Student
        exclude = ['name', 'age']

