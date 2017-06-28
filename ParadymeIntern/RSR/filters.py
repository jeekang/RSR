import django_filters
from .models import Person
from django import forms

class PersonFilter(django_filters.FilterSet):
    language = django_filters.CharFilter(name='language', lookup_expr='icontains')
    skills = django_filters.CharFilter(name='skills', lookup_expr='icontains')
    certificate = django_filters.CharFilter(name='certificate', lookup_expr='icontains')
    awards = django_filters.CharFilter(name='awards', lookup_expr='icontains')
    conference = django_filters.CharFilter(name='conference', lookup_expr='icontains')
    prior_company = django_filters.CharFilter(name='prior_company', lookup_expr='icontains')

    class Meta:
        model = Person
        fields = ['school', 'school_level', 'graduation_year', 'graduation_month', 'major', 'skills',
                  'language', 'certificate', 'awards', 'conference', 'prior_company', 'work_authorization',
                  'security_clearance']

