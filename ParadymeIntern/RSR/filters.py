import django_filters
from .models import *
from django import forms

class UploadListFilter(django_filters.FilterSet):

	TYPERESUME_CHOICES = (('Employee', 'Employee'),
	('Intern', 'Intern'),
	('Prospective Employee', 'Prospective Employee'),
	('Prospective Intern', 'Prospective Intern'),

)
	type = django_filters.ChoiceFilter(choices=TYPERESUME_CHOICES)
	class Meta:
	    model = Document
	    fields = ['firstname','lastname','type']
	    order_by = ['pk']


class PersonFilter(django_filters.FilterSet):
    SchoolAttend = django_filters.ModelChoiceFilter(name='persontoschool__SchoolID', queryset=School.objects.all(),
                                                    to_field_name='id')
    GraduateDate = django_filters.ModelChoiceFilter(name='persontoschool__GradDate',
                                                    queryset=PersonToSchool.objects.values_list('GradDate',flat=True).distinct(),
                                                    to_field_name='GradDate')
    Major = django_filters.ModelChoiceFilter(name='persontoschool__MajorID', queryset=Major.objects.all())
    DegreeLevel = django_filters.ModelChoiceFilter(name='school__DegreeLevel',
                                                   queryset=School.objects.values_list('DegreeLevel',flat=True).distinct(),
                                                   to_field_name='DegreeLevel')
    # skills = django_filters.CharFilter(name='skills', lookup_expr='icontains')
    # certificate = django_filters.CharFilter(name='certificate', lookup_expr='icontains')
    # awards = django_filters.CharFilter(name='awards', lookup_expr='icontains')
    # professional_development = django_filters.CharFilter(name='professional_development', lookup_expr='icontains')
    # prior_company = django_filters.CharFilter(name='prior_company', lookup_expr='icontains')
    # title = django_filters.CharFilter(name='title', lookup_expr='icontains')
    # gpa_gt = django_filters.NumberFilter(name='gpa', lookup_expr='gt')
    # year_of_experience_gt = django_filters.NumberFilter(name='year_of_experience', lookup_expr='gt')

    class Meta:
        model = Person
        fields = ['SchoolAttend','GraduateDate','Major','DegreeLevel']
