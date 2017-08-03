# -*- coding: utf-8 -*-
from django import forms
import os
from .models import *

class PersonForm(forms.ModelForm):

    class Meta:

        model = Person
        exclude=('Resume',)
        fields = '__all__'
    	
#### EDIT TEAM DO NOT USE THESE, THESE ARE FOR ADD FORMS ###
class NewPersontoSkillForm(forms.ModelForm):

    class Meta:
     	model = PersonToSkills
     	exclude = ('PersonID',)
     	fields = ('YearsOfExperience',)
class NewPersontoCompanyForm(forms.ModelForm):
	class Meta:
		model = PersonToCompany
		exclude = ('PersonID', 'CompanyID')
		fields = '__all__'

class NewPersontoSchoolForm(forms.ModelForm):
	class Meta:
		model = PersonToSchool
		exclude = ('PersonID', 'SchoolID','MajorID')
		fields = '__all__'
class NewMajorForm(forms.ModelForm):
	class Meta:
		model = Major
		fields = ('Name','Dept','MajorMinor')
class NewSchoolForm(forms.ModelForm):
	class Meta:
		model = School
		fields = ('Name','DegreeLevel',)
class NewPersontoCourseForm(forms.ModelForm):
	class Meta:
		model = PersonToCourse
		exclude = ('PersonID', 'CourseID')
		fields = '__all__'
class NewPersontoSideForm(forms.ModelForm):
	class Meta:
		model = PersonToSide
		exclude = ('PersonID', 'SideID')
		fields = '__all__'
class NewPersontoAwardForm(forms.ModelForm):
	class Meta:
		model = PersonToSide
		exclude = ('PersonID', 'AwardID')
		fields = '__all__'
class NewPersontoClubForm(forms.ModelForm):
	class Meta:
		model = PersonToClubs_Hobbies
		exclude = ('PersonID', 'CHID')
		fields = '__all__'
class NewPersontoVolunteerForm(forms.ModelForm):
	class Meta:
		model = PersonToVolunteering
		exclude = ('PersonID', 'VolunID')
		fields = '__all__'
class NewPersontoProfessionalForm(forms.ModelForm):
	class Meta:
		model = PersonToProfessionalDevelopment
		exclude = ('PersonID', 'ProfID')
		fields = '__all__'

#### USE BELOW FOR EDIT ###
	
class PersontoSkillForm(forms.ModelForm):
	class Meta:
		model = PersonToSkills
		fields = '__all__'

class PersontoCompanyForm(forms.ModelForm):
	class Meta:
		model = PersonToCompany
		fields = '__all__'

class PersontoAwardForm(forms.ModelForm):
	class Meta:
		model = PersonToAwards
		fields = '__all__'

class PersontoClubForm(forms.ModelForm):
	class Meta:
		model = PersonToClubs_Hobbies
		fields = '__all__'

class PersontoVolunteeringForm(forms.ModelForm):
	class Meta:
		model = PersonToVolunteering
		fields = '__all__'
class PersontoProfessionalForm(forms.ModelForm):
	class Meta:
		model = PersonToProfessionalDevelopment
		fields = '__all__'
class PersontoSideForm(forms.ModelForm):
	class Meta:
		model = PersonToSide
		fields = '__all__'
class PersontoLanguageForm(forms.ModelForm):
	class Meta:
		model = PersonToLanguage
		fields = '__all__'
class PersontoClearanceForm(forms.ModelForm):
	class Meta:
		model = PersonToClearance
		fields = '__all__'
class PersontoCourseForm(forms.ModelForm):
	class Meta:
		model = PersonToCourse
		fields = '__all__'
class PersontoSchoolForm(forms.ModelForm):
	class Meta:
		model = PersonToSchool
		fields = '__all__'



class CommentsForm(forms.ModelForm):
	Comments = forms.CharField( widget=forms.Textarea )
	class Meta:
		model = Person
		fields =('Comments',)

class DocumentForm(forms.Form):
	pwd = os.path.dirname(__file__)
	with open(pwd+"/static/config/config.txt") as myfile:
		dataconfig="".join(line.rstrip() for line in myfile)
    
	docfile = forms.FileField(widget=forms.FileInput(attrs={'accept':dataconfig}),label='Select a file:')

class SkillForm(forms.ModelForm):
	class Meta:
		model = Skills
		fields = '__all__'
		

class CompanyForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = '__all__'

class AwardForm(forms.ModelForm):
	class Meta:
		model = Awards
		fields = '__all__'

class ClubForm(forms.ModelForm):
	class Meta:
		model = Clubs_Hobbies
		fields = '__all__'

class VolunteeringForm(forms.ModelForm):
	class Meta:
		model = Volunteering
		fields = ('Name',)
class ProfessionalForm(forms.ModelForm):
	class Meta:
		model = ProfessionalDevelopment
		fields = ('Name',)
class SideForm(forms.ModelForm):
	class Meta:
		model = SideProject
		fields = '__all__'
class LanguageForm(forms.ModelForm):
	class Meta:
		model = LanguageSpoken
		fields = '__all__'
class ClearanceForm(forms.ModelForm):
	class Meta:
		model = Clearance
		fields = '__all__'
class CourseForm(forms.ModelForm):
	class Meta:
		model = Coursework
		fields = '__all__'
class SchoolForm(forms.ModelForm):
	class Meta:
		model = School
		fields = '__all__'
class MajorForm(forms.ModelForm):
	class Meta:
		model = Major
		fields = '__all__'
