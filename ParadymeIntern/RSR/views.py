from .models import *

# Create your views here.
#=======
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from RSR.models import *
from RSR.forms import DocumentForm
from .filters import PersonFilter

# UI/INGEST TEAM
def main(request):
    return render(request, 'main.html')

def uploaddoc(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return HttpResponseRedirect(reverse('RSR:uploaddoc'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    return render(request,'index.html',{'documents': documents, 'form': form})

def user_acc_cont (request):
    return render(request, 'acc_cont.html')

def uploadlist (request):
    documents = Document.objects.all()
    context ={'documents':documents}
    return render(request,'uploadlist.html',context)

# OCR TEAM
def ocr (request):
    return render(request, 'ocr.html')

# PARSING TEAM
def parsing(request):
    return render(request, 'parsing.html')

# SEARCH/EXPORT TEAM
def search (request):
    f = PersonFilter(request.GET, queryset=Person.objects.all())
    return render(request, 'SearchExport/index.html', {'filter': f})

class detail(generic.DetailView):
    model = Person
    template_name = 'SearchExport/detail.html'

def export(request):
    return render (request, 'export.html')

# LINK ANALYSIS TEAM
def linkanalysis(request):
    return render(request, 'linkanalysis.html')
