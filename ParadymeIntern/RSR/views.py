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
        field_name_set = []
        # Storing all fields of person into a list
        for field in Person._meta.fields:
            field_name = field.get_attname()
            # I don't want the id of a field rather I want the value
            if field_name == "id":
                continue
            field_name_set.append(field_name)
        # Q() aka q objects are ways to filter more than 1 field at a time consecutively
        q_objects = []
        # I will create a list of q objects
        for name in field_name_set:
            if name.find('_id') != -1:
                # Foreign keys require me to define the field of the Person and the field of the Foreign key I'm trying
                # to access
                name = name.replace('_id', '')
                q_objects.append(Q(**{name + '__' + name + '__icontains': query}))
            else:
                q_objects.append(Q(**{name + '__icontains': query}))
        q_object = q_objects.pop()
        # From the list I will create 1 huge q object containing Q(field1) or Q(field2) etc |= denotes equal or.
        for name2 in q_objects:
            q_object |= name2
        # So q_object looks something lke this Q(field1__contains=text)|Q(field2__contains=text) and so on. It checks
        # if each field contains the text if at least 1 field contains the text the person object will be returned in
        # a query set.
        query_set = query_set.filter(q_object)
    # The filtered query_set is then put through more filters from django
    f = PersonFilter(request.GET, query_set)
    return render(request, 'SearchExport/index.html', {'filter': f})


class detail(generic.DetailView):
    model = Person
    template_name = 'SearchExport/detail.html'


def export(request):
    return render(request, 'export.html')


# LINK ANALYSIS TEAM
def linkanalysis(request):
    return render(request, 'linkanalysis.html')
