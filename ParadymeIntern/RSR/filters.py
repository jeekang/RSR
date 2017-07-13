import django_filters
from .models import *
from django_filters.widgets import LinkWidget, LookupTypeWidget, RangeWidget
from django import forms


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
    GPA = django_filters.ModelChoiceFilter(name='persontoschool__GPA',
                                                    queryset=PersonToSchool.objects.values_list('GPA',flat=True).distinct(),
                                                    to_field_name='GPA', lookup_expr='gte')
    Language = django_filters.ModelChoiceFilter(name='persontolanguage__LangID', queryset=LanguageSpoken.objects.all())
    Skills = django_filters.ModelChoiceFilter(name ='persontoskills__SkillsID', queryset=Skills.objects.all())
    YearOfExperienceForSkill = django_filters.ModelChoiceFilter(name='persontoskills__YearsOfExperience',
                                                                queryset=PersonToSkills.objects.values_list('YearsOfExperience',flat=True).distinct(),
                                                                to_field_name='YearsOfExperience')
    ProfessionalDevelopment = django_filters.ModelChoiceFilter(name='persontoprofessionaldevelopment__ProfID',
                                                               queryset=ProfessionalDevelopment.objects.all())
    Award = django_filters.ModelChoiceFilter(name='persontoawards__AwardID', queryset=Awards.objects.all())
    CompanyWorked = django_filters.ModelChoiceFilter(name='persontocompany__CompanyID', queryset=Company.objects.all())
    Title = django_filters.ModelChoiceFilter(name='persontocompany__Title',
                                             queryset=PersonToCompany.objects.values_list('Title',flat=True).distinct(),
                                             to_field_name='Title')
    SecurityClearance = django_filters.ModelChoiceFilter(name='persontoclearance__ClearanceLevel', queryset=Clearance.objects.all())


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
        fields = ['SchoolAttend', 'GraduateDate', 'Major', 'DegreeLevel', 'GPA', 'Language', 'Skills',
                  'YearOfExperienceForSkill', 'ProfessionalDevelopment', 'Award', 'CompanyWorked', 'Title']
