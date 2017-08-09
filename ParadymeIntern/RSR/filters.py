# this file is for search/export team to create filters
import django_filters
from .models import *
from django import forms
from dal import autocomplete
from django.forms import TextInput
from django.db.models import Q

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

WORKAUTHORIZATION_CHOICES = (
        ('Citizenship', 'Citizenship'),
        ('Permanent Resident', 'Permanent Resident'),
        ('Visa', 'Visa')
    )

class PersonFilter(django_filters.FilterSet):
    SchoolAttend = django_filters.ModelChoiceFilter(name='persontoschool__SchoolID', queryset=School.objects.all().order_by('Name'),
                                                    to_field_name='Name')
    #SchoolAttend = django_filters.ModelChoiceFilter(name='school__Name',
                                                    #queryset=School.objects.values_list('Name',flat=True),
                                                    #to_field_name='Name', lookup_expr='icontains', widget=forms.TextInput)
    GraduateDate = django_filters.ModelChoiceFilter(name='persontoschool__GradDate',
                                                    queryset=PersonToSchool.objects.values_list('GradDate',flat=True).
                                                    distinct().order_by('GradDate'),
                                                    to_field_name='GradDate')
    Major = django_filters.ModelChoiceFilter(name='persontoschool__MajorID', queryset=Major.objects.all().order_by('Name').distinct())
    DegreeLevel = django_filters.ModelChoiceFilter(name='persontoschool__SchoolID__DegreeLevel',
                                                   queryset=School.objects.values_list('DegreeLevel',flat=True).distinct(),
                                                   to_field_name='DegreeLevel')
    GPAlb = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='gte')
    GPAub = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='lt')
    Coursework = django_filters.ModelChoiceFilter(name='persontocourse__Desc',
                                                  queryset=PersonToCourse.objects.values_list('Desc', flat=True).distinct().order_by('Desc'),
                                                  to_field_name='Desc')
    Language = django_filters.ModelMultipleChoiceFilter(name='persontolanguage__LangID',
                                                queryset=LanguageSpoken.objects.all(),
                                                widget=autocomplete.ModelSelect2Multiple(url='RSR:LanguageSpoken-autocomplete'), conjoined=True)

    Skills = django_filters.ModelMultipleChoiceFilter(name='persontoskills__SkillsID',
                                              queryset=Skills.objects.all().order_by('Name').distinct(),
                                              widget=autocomplete.ModelSelect2Multiple(url='RSR:Skills-autocomplete'), conjoined=True)

    YearOfExperienceForSkill = django_filters.ModelChoiceFilter(name='persontoskills__YearsOfExperience',
                                                                lookup_expr='gte',
                                                                queryset=PersonToSkills.objects.values_list('YearsOfExperience',flat=True).
                                                                order_by('YearsOfExperience').distinct(),to_field_name='YearsOfExperience')
    #YearOfExperienceForSkill = django_filters.NumberFilter(name='persontoskills__YearsOfExperience', lookup_expr='gte')
    ProfessionalDevelopment = django_filters.ModelChoiceFilter(name='persontoprofessionaldevelopment__ProfID',
                                                               queryset=ProfessionalDevelopment.objects.all(),
                                                               widget=autocomplete.ModelSelect2(url='RSR:ProfessionalDevelopment-autocomplete'))
    #ProfessionalDevelopment = django_filters.ModelChoiceFilter(name='professionaldevelopment__Name',
    #                                                           queryset=ProfessionalDevelopment.objects.values_list('Name', flat=True).order_by('Name').distinct(),
    #                                                           to_field_name='Name',
    #                                                           widget=autocomplete.ModelSelect2(url='RSR:ProfessionalDevelopment-autocomplete'))
    #ProfessionalDevelopment = django_filters.CharFilter(name='professionaldevelopment__Name', lookup_expr='icontains')
    Award = django_filters.ModelChoiceFilter(name='persontoawards__AwardID',
                                             queryset=Awards.objects.all().order_by('Name').distinct(),
                                             to_field_name='Name')
    CompanyWorked = django_filters.ModelChoiceFilter(name='persontocompany__CompanyID',
                                                     queryset=Company.objects.all(),
                                                     widget=autocomplete.ModelSelect2(url='RSR:Company-autocomplete'))
    Title = django_filters.ModelChoiceFilter(name='persontocompany__Title',
                                             queryset=PersonToCompany.objects.values_list('Title',flat=True).
                                             distinct().order_by('Title'),
                                             to_field_name='Title')
    #Volunteering = django_filters.CharFilter(name='volunteering__Name',lookup_expr='icontains')
    Volunteering = django_filters.ModelChoiceFilter(name='persontovolunteering__VolunID',
                                                    queryset=Volunteering.objects.all(),
                                                    widget=autocomplete.ModelSelect2(url='RSR:Volunteering-autocomplete'))
    Club_Hobby = django_filters.ModelChoiceFilter(name='persontoclubshobbies_set__CHID',
                                                  queryset=Clubs_Hobbies.objects.all().distinct().order_by('Name'),
                                                  to_field_name='Name')
    SecurityClearance = django_filters.ModelChoiceFilter(name='persontoclearance__ClearanceLevel',
                                                         queryset=Clearance.objects.all().distinct())
    WorkAuthorization = django_filters.ChoiceFilter(name='WorkAuthorization', choices=WORKAUTHORIZATION_CHOICES)
    Name=django_filters.ModelChoiceFilter(name='Name',
                                          queryset=Person.objects.all(),
                                          widget=autocomplete.ModelSelect2(url='RSR:SearchBar-autocomplete'))


    class Meta:
        model = Person
        fields = ['SchoolAttend', 'GraduateDate', 'Major', 'DegreeLevel', 'GPAlb', 'GPAub','Language', 'Skills',
                  'YearOfExperienceForSkill', 'ProfessionalDevelopment', 'Award', 'CompanyWorked', 'Title',
                  'SecurityClearance', 'Volunteering', 'Club_Hobby', 'Name','WorkAuthorization', 'Coursework']
