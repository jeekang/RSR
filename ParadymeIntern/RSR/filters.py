import django_filters
from .models import Person

class PersonFilter(django_filters.FilterSet):
    school = django_filters.ModelChoiceFilter(name='school', queryset=Person.objects.order_by().
                                              values_list('school', flat=True).distinct())
    school_level = django_filters.ModelChoiceFilter(name='school_level', queryset=Person.objects.order_by().
                                                    values_list('school_level', flat=True).distinct())
    major = django_filters.ModelChoiceFilter(name='major', queryset=Person.objects.order_by().
                                             values_list('major', flat=True).distinct())
    work_authorization = django_filters.ModelChoiceFilter(name='work_authorization', queryset=Person.objects.order_by().
                                                          values_list('work_authorization', flat=True).distinct())
    security_clearance = django_filters.ModelChoiceFilter(name='security_clearance', queryset=Person.objects.order_by().
                                                          values_list('security_clearance', flat=True).distinct())
    graduation_year = django_filters.ModelChoiceFilter(name='graduation_year', queryset=Person.objects.order_by().
                                                       values_list('graduation_year', flat=True).distinct())
    graduation_month = django_filters.ModelChoiceFilter(name='graduation_month', queryset=Person.objects.order_by().
                                                        values_list('graduation_month', flat=True).distinct())
    language = django_filters.CharFilter(name='language', lookup_expr='icontains')
    skills = django_filters.CharFilter(name='skills', lookup_expr='icontains')
    certificate = django_filters.CharFilter(name='certificate', lookup_expr='icontains')
    awards = django_filters.CharFilter(name='awards', lookup_expr='icontains')
    professional_development = django_filters.CharFilter(name='professional_development', lookup_expr='icontains')
    prior_company = django_filters.CharFilter(name='prior_company', lookup_expr='icontains')

    class Meta:
        model = Person
        fields = ['school', 'school_level', 'graduation_year', 'graduation_month', 'major', 'skills',
                  'language', 'certificate', 'awards', 'professional_development', 'prior_company', 'work_authorization',
                  'security_clearance']

