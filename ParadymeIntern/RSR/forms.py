# -*- coding: utf-8 -*-
from django import forms
import os
from .models import *

class PersonForm(forms.ModelForm):

    class Meta:

        model = Person
        fields = '__all__'
		
class DocumentForm(forms.Form):
	pwd = os.path.dirname(__file__)
	with open(pwd+"/static/config/config.txt") as myfile:
		dataconfig="".join(line.rstrip() for line in myfile)
    
	docfile = forms.FileField(widget=forms.FileInput(attrs={'accept':dataconfig}),label='Select a file:')
