import django_filters
from .models import Person
from django import forms

class PersonFilter(django_filters.FilterSet):

    language = django_filters.CharFilter(name='language',lookup_expr='icontains')
    skills = django_filters.CharFilter(name='skills', lookup_expr='icontains')
    certificate = django_filters.CharFilter(name='certificate', lookup_expr='icontains')
    awards = django_filters.CharFilter(name='awards', lookup_expr='icontains')
    professional_development = django_filters.CharFilter(name='professional_development', lookup_expr='icontains')
    prior_company = django_filters.CharFilter(name='prior_company', lookup_expr='icontains')
    title = django_filters.CharFilter(name='title', lookup_expr='icontains')
    gpa_gt = django_filters.NumberFilter(name='gpa', lookup_expr='gt')
    year_of_experience_gt = django_filters.NumberFilter(name='year_of_experience', lookup_expr='gt')

    class Meta:
        model = Person
        fields = ['Name',]
