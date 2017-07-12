import django_filters
from .models import *

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