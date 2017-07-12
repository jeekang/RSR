import django_filters
from .models import *

class UploadListFilter(django_filters.FilterSet):
    class Meta:
	    model = Document
	    fields = '__all__'
	    order_by = ['pk']