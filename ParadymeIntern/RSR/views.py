from .models import *

# Create your views here.
# =======
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from RSR.models import *
from RSR.forms import DocumentForm
from .filters import PersonFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from RSR.persondetails import Detail
from dal import autocomplete


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
    return render(request, 'index.html', {'documents': documents, 'form': form})


def user_acc_cont(request):
    return render(request, 'acc_cont.html')


def uploadlist(request):
    documents = Document.objects.all()
    context = {'documents': documents}
    return render(request, 'uploadlist.html', context)


def listdelete(request, template_name='uploadlist.html'):
    docId = request.POST.get('docfile', None)
    documents = get_object_or_404(Document, pk=docId)
    if request.method == 'POST':
        documents.delete()
        return HttpResponseRedirect(reverse('uploadlist'))

    return render(request, template_name, {'object': documents})


# OCR TEAM
def ocr(request):
    return render(request, 'ocr.html')


# PARSING TEAM
def parsing(request):
    return render(request, 'parsing.html')


# SEARCH/EXPORT TEAM
def search(request):
    query_set = Person.objects.order_by('Name').distinct()
    personFilter = PersonFilter(request.GET, query_set)
    return render(request, 'SearchExport/search.html', {'personFilter': personFilter})

class ProfessionalDevelopmentAutocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for ProfessionalDevelopment class
    def get_queryset(self):
        qs = ProfessionalDevelopment.order_by('Name').distinct()

        if self.q:
            qs = qs.filter(Name__istartswith=self.q)
        return qs

class Skillsutocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Skills class
    def get_queryset(self):
        qs = Skills.objects.order_by('Name').distinct()

        if self.q:
            qs = qs.filter(Name__istartswith=self.q)
        return qs

class Volunteeringautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Volunteering class
    def get_queryset(self):
        qs = Volunteering.objects.order_by('Name').distinct()
        if self.q:
            qs = qs.filter(Name__istartswith=self.q)
        return qs

class SearchBarautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Search Bar that sorts by Person Names
    def get_queryset(self):
        qs = Person.objects.order_by('Name').distinct()
        if self.q:
            qs = qs.filter(Name__istartswith=self.q)
        return qs

class Languageautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for LanguageSpoken class
    def get_queryset(self):
        qs = LanguageSpoken.objects.order_by('Language').distinct()
        if self.q:
            qs = qs.filter(Language__istartswith=self.q)
        return qs

class Companyautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Company class
    def get_queryset(self):
        qs = Company.objects.order_by('Name').distinct()
        if self.q:
            qs = qs.filter(Name__istartswith=self.q)
        return qs

def detail(request,pk):
    # Get the current person object using pk or id
    person = get_object_or_404(Person,pk=pk)
    related_obj_list=Detail(person)
    return render(request, 'SearchExport/detail.html', {'person':person, 'list':related_obj_list})


def export(request):
    return render(request, 'export.html')


# LINK ANALYSIS TEAM
def linkanalysis(request):
    return render(request, 'linkanalysis.html')
