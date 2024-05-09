

import django_filters
from .models import Book

from django import forms
from .models import Book, Stage, ClassLevel, Supplier

import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.ModelChoiceFilter(field_name='title', queryset=Book.objects.all(), label='اسم المادة الدراسية')
    source = django_filters.ModelChoiceFilter(field_name='source', queryset=Book.objects.all(), label='مصدر التوريد')
    supplier = django_filters.ModelChoiceFilter(field_name='supplier', queryset=Supplier.objects.all(), label='اسم المورد')
    stage = django_filters.ModelChoiceFilter(field_name='stage', queryset=Stage.objects.all(), label='اسم المرحلة الدراسية')
    class_level = django_filters.ModelChoiceFilter(field_name='class_level', queryset=ClassLevel.objects.all(), label='اسم الصف الدراسي')
    term = django_filters.ChoiceFilter(choices=Book.TERM_CHOICES, label='الترم الدراسي')
    received_date__gte = django_filters.DateFilter(field_name='received_date', lookup_expr='gte', label='تاريخ الاستلام (من)')
    received_date__lte = django_filters.DateFilter(field_name='received_date', lookup_expr='lte', label='تاريخ الاستلام (إلى)')

    class Meta:
        model = Book
        fields = {
            'received_quantity': ['exact', 'gte', 'lte'],
            'available_quantity': ['exact', 'gte', 'lte'],
            'term': ['exact'],
            'received_date': ['exact', 'gte', 'lte'],
        }

