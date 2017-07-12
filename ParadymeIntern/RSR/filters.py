import django_filters
from .models import *

class UploadListFilter(django_filters.FilterSet):
    class Meta:
	    model = Document
	    fields = ['firstname','lastname','type']
	    order_by = ['pk']