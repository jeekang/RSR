# this file is for search/export team to create filters
import django_filters
from .models import *
from django import forms
from dal import autocomplete


class PersonFilter(django_filters.FilterSet):
    SchoolAttend = django_filters.ModelChoiceFilter(name='persontoschool__SchoolID', queryset=School.objects.all().order_by('Name'),
                                                    to_field_name='id')
    #SchoolAttend = django_filters.ModelChoiceFilter(name='school__Name',
                                                    #queryset=School.objects.values_list('Name',flat=True),
                                                    #to_field_name='Name', lookup_expr='icontains', widget=forms.TextInput)
    GraduateDate = django_filters.ModelChoiceFilter(name='persontoschool__GradDate',
                                                    queryset=PersonToSchool.objects.values_list('GradDate',flat=True).
                                                    distinct().order_by('GradDate'),
                                                    to_field_name='GradDate')
    Major = django_filters.ModelChoiceFilter(name='persontoschool__MajorID', queryset=Major.objects.all().order_by('Name'))
    DegreeLevel = django_filters.ModelChoiceFilter(name='school__DegreeLevel',
                                                   queryset=School.objects.values_list('DegreeLevel',flat=True).distinct(),
                                                   to_field_name='DegreeLevel')
    GPAlb = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='gte')
    GPAub = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='lt')
    Language = django_filters.ModelChoiceFilter(name='persontolanguage__LangID',
                                                queryset=LanguageSpoken.objects.all().order_by('Language'))
    Skills = django_filters.ModelChoiceFilter(name='persontoskills__SkillsID',
                                              queryset=Skills.objects.all().order_by('Name').distinct(),
                                              widget=autocomplete.ModelSelect2(url='RSR:Skills-autocomplete'))
    YearOfExperienceForSkill = django_filters.ModelChoiceFilter(name='persontoskills__YearsOfExperience',
                                                                queryset=PersonToSkills.objects.values_list('YearsOfExperience',flat=True).
                                                                distinct().order_by('YearsOfExperience'),to_field_name='YearsOfExperience')
    #YearOfExperienceForSkill = django_filters.NumberFilter(name='persontoskills__YearsOfExperience', lookup_expr='gte')
    ProfessionalDevelopment = django_filters.ModelChoiceFilter(name='persontoprofessionaldevelopment__ProfID',
                                                               queryset=ProfessionalDevelopment.objects.all().order_by('Name'),
                                                               widget=autocomplete.ModelSelect2(url='RSR:ProfessionalDevelopment-autocomplete'))
    #ProfessionalDevelopment = django_filters.ModelChoiceFilter(name='professionaldevelopment__Name',
    #                                                           queryset=ProfessionalDevelopment.objects.values_list('Name', flat=True).order_by('Name').distinct(),
    #                                                           to_field_name='Name',
    #                                                           widget=autocomplete.ModelSelect2(url='RSR:ProfessionalDevelopment-autocomplete'))
    #ProfessionalDevelopment = django_filters.CharFilter(name='professionaldevelopment__Name', lookup_expr='icontains')
    Award = django_filters.ModelChoiceFilter(name='persontoawards__AwardID',
                                             queryset=Awards.objects.all().order_by('Name'))
    CompanyWorked = django_filters.ModelChoiceFilter(name='persontocompany__CompanyID',
                                                     queryset=Company.objects.all().order_by('Name'))
    Title = django_filters.ModelChoiceFilter(name='persontocompany__Title',
                                             queryset=PersonToCompany.objects.values_list('Title',flat=True).
                                             distinct().order_by('Title'),
                                             to_field_name='Title')
    #Volunteering = django_filters.CharFilter(name='volunteering__Name',lookup_expr='icontains')
    Volunteering = django_filters.ModelChoiceFilter(name='persontovolunteering__VolunID',
                                                    queryset=Volunteering.objects.all().order_by('Name'),
                                                    widget=autocomplete.ModelSelect2(url='RSR:Volunteering-autocomplete'))
    Club_Hobby = django_filters.ModelChoiceFilter(name='persontoclubshobbies_set__CHID',
                                                  queryset=Clubs_Hobbies.objects.all().distinct().order_by('Name'))
    SecurityClearance = django_filters.ModelChoiceFilter(name='persontoclearance__ClearanceLevel',
                                                         queryset=Clearance.objects.all().order_by('ClearanceLevel'))



    class Meta:
        model = Person
        fields = ['SchoolAttend', 'GraduateDate', 'Major', 'DegreeLevel', 'GPAlb', 'GPAub','Language', 'Skills',
                  'YearOfExperienceForSkill', 'ProfessionalDevelopment', 'Award', 'CompanyWorked', 'Title',
                  'SecurityClearance', 'Volunteering', 'Club_Hobby']
