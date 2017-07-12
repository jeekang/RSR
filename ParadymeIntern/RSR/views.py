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
    query_set = Person.objects.all()
    query = request.GET.get("q")
    if query:
        query_set=query_set.filter(Name__icontains=query)
    # The filtered query_set is then put through more filters from django
    personFilter = PersonFilter(request.GET, query_set)
    return render(request, 'SearchExport/search.html', {'personFilter': personFilter})


def detail(request,pk):
    # Get the current person object using pk or id
    person = get_object_or_404(Person,pk=pk)
    related_obj_list=[]
    # This is the related_set names, I add the personto and _set part to it later on for preference purposes only
    relatedNames = ['school','course', 'certificate', 'side', 'skills', 'language'
        , 'clearence', 'company', 'awards', 'clubshobbies', 'volunteering']
    # This is the foreign key reference to the models
    modelReferences = ['SchoolID', 'CourseID', 'CertID', 'SideID', 'SkillsID', 'LangID', 'ClearenceLevel',
                       'CompanyName', 'AwardName', 'CHName', 'VolunName']
    # Im adding major beforehand to the list since it's a special case
    for major in person.persontoschool_set.all():
        related_obj_list.append('Major: '+ str(major.MajorID))
    # Loops through every model
    position=0
    for related in relatedNames:
        # Get the related set of each model
        # The default related set is the name of intermediary table, lowercased + _set
        # The related set is used to reverse foreign keys and you access it by currentmodel.related_set where
        # the related_set is where the foreign key to current model stems from
        string = 'personto'+related+'_set'
        related_obj = eval('person.'+string)
        # Related_obj cannot be iterated unless put in a query set so I put in a query set using all()
        related_obj = related_obj.all()
        # There should only be 1 object in this query set
        for item in related_obj:
            # I want to do something grab the exact field of the item so I use getattr
            item=getattr(item,modelReferences[position])
            # Finally I add the string I want to be displayed into related_obj_list which I will iterate through in
            # details template
            related_obj_list.append(related.capitalize()+': ' +str(item))
        position+=1
    return render(request, 'SearchExport/detail.html', {'person':person, 'list':related_obj_list})


def export(request):
    return render(request, 'export.html')


# LINK ANALYSIS TEAM
def linkanalysis(request):
    return render(request, 'linkanalysis.html')
