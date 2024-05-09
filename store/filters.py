import django_filters
from django_filters import DateFromToRangeFilter
from .models import AcademicYear, ClassLevel, Classroom, Stage, Student
from django_filters import DateRangeFilter
from django_filters.widgets import RangeWidget
from django_filters import DateFromToRangeFilter
from django.db.models import Sum, F, Value
from django.db.models.functions import Concat
from django_filters.widgets import DateRangeWidget
from django import forms
from django.utils.translation import gettext_lazy as _
from store.forms import StudentForm


class StudentFilter(django_filters.FilterSet):
    # ترتيب الحقول بطريقة منطقية
    class Meta:
        model = Student
        fields = {
            'academic_year': ['exact'],
            'name': ['exact'],
            'national_id': ['exact'],
            'stage': ['exact'],
            'class_level': ['exact'],
            'section': ['exact'],
        }
        help_texts = {
            'academic_year': _('Filter by academic year'),
            'name': _('Filter by student name'),
            'national_id': _('Filter by national ID'),
            'stage': _('Filter by stage'),
            'class_level': _('Filter by class level'),
            'section': _('Filter by section'),
        }
    academic_year = django_filters.ModelChoiceFilter(
        field_name='academic_year',
        queryset=AcademicYear.objects.all(),
        label=_('Academic Year'),
    )

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='اسم الطالب')
    stage = django_filters.ModelChoiceFilter(field_name='stage', queryset=Stage.objects.all(), label='المرحلة الدراسية')
    class_level = django_filters.ModelChoiceFilter(field_name='class_level', queryset=ClassLevel.objects.all(), label='الصف الدراسي')
    section = django_filters.ModelChoiceFilter(field_name='section', queryset=Classroom.objects.all(), label='الفصل الدراسي')
    academic_year = django_filters.ModelChoiceFilter(field_name='academic_year', queryset=AcademicYear.objects.all(), label='السنة الدراسية')
    national_id = django_filters.CharFilter(field_name='national_id', lookup_expr='exact', label='الرقم القومي')

