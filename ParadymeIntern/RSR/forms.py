# -*- coding: utf-8 -*-
from django import forms
import os
from .models import *

class PersonForm(forms.ModelForm):

    class Meta:

        model = Person
        fields = '__all__'

class PersontoSkillForm(forms.ModelForm):

    class Meta:
     	model = PersonToSkills
     	exclude = ('PersonID',)
     	fields = ('YearsOfExperience',)


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
		