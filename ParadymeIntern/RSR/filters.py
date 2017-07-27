import django_filters
from .models import *
from django import forms
from django.forms import TextInput

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
      widgets = { 'firstname':TextInput(attrs = {'class':'form-control','placeholder': 'First Name','style':'color:#000'})

      }
      order_by = ['pk']



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
    #GPA = django_filters.ModelChoiceFilter(name='persontoschool__GPA',
    #                                                queryset=PersonToSchool.objects.values_list('GPA',flat=True).distinct(),
    #                                                to_field_name='GPA', lookup_expr='gte',
    #                                       widget=RangeWidget(attrs={'placeholder': '0.0'}))
    GPAlb = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='gte')
    GPAub = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='lt')
    Language = django_filters.ModelChoiceFilter(name='persontolanguage__LangID',
                                                queryset=LanguageSpoken.objects.all().order_by('Language'))
    Skills = django_filters.ModelChoiceFilter(name ='persontoskills__SkillsID',
                                              queryset=Skills.objects.all().order_by('Name').distinct())
    YearOfExperienceForSkill = django_filters.ModelChoiceFilter(name='persontoskills__YearsOfExperience',
                                                                queryset=PersonToSkills.objects.
                                                                values_list('YearsOfExperience',flat=True).
                                                                distinct().order_by('YearsOfExperience'),
                                                                to_field_name='YearsOfExperience')
    #ProfessionalDevelopment = django_filters.ModelChoiceFilter(name='persontoprofessionaldevelopment__ProfID',
    #                                                           queryset=ProfessionalDevelopment.objects.all().order_by('Name'))
    #ProfessionalDevelopment = django_filters.ModelChoiceFilter(name='professionaldevelopment__Name',
    #                                                           queryset=ProfessionalDevelopment.objects.values_list('Name', flat=True),
    #                                                          to_field_name='Name', lookup_expr='icontains',
    #                                                          widget=forms.TextInput)
    ProfessionalDevelopment = django_filters.CharFilter(name='professionaldevelopment__Name', lookup_expr='icontains')
    Award = django_filters.ModelChoiceFilter(name='persontoawards__AwardID',
                                             queryset=Awards.objects.all().order_by('Name'))
    CompanyWorked = django_filters.ModelChoiceFilter(name='persontocompany__CompanyID',
                                                     queryset=Company.objects.all().order_by('Name'))
    Title = django_filters.ModelChoiceFilter(name='persontocompany__Title',
                                             queryset=PersonToCompany.objects.values_list('Title',flat=True).
                                             distinct().order_by('Title'),
                                             to_field_name='Title')
    Volunteering = django_filters.CharFilter(name='volunteering__Name',lookup_expr='icontains')
    Club_Hobby = django_filters.ModelChoiceFilter(name='persontoclubshobbies_set__CHID',
                                                   queryset=Clubs_Hobbies.objects.all().distinct().order_by('Name'))
    SecurityClearance = django_filters.ModelChoiceFilter(name='persontoclearance__ClearanceLevel',
                                                         queryset=Clearance.objects.all().order_by('ClearanceLevel'))


    class Meta:
        model = Person
        fields = ['SchoolAttend', 'GraduateDate', 'Major', 'DegreeLevel', 'GPAlb', 'GPAub','Language', 'Skills',
                   'YearOfExperienceForSkill', 'ProfessionalDevelopment', 'Award', 'CompanyWorked', 'Title',
                   'SecurityClearance', 'Volunteering', 'Club_Hobby']
