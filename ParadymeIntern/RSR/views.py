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
        field_name_set=[]
        for field in Person._meta.fields:
            field_name = field.get_attname()
            if field_name == "id":
                continue
            field_name_set.append(field_name)
        q_objects=[]
        for name in field_name_set:
            if name.find('_id')!=-1:
                name = name.replace('_id', '')
                q_objects.append(Q(**{name+'__'+name+'__icontains':query}))
            else:
                q_objects.append(Q(**{name+'__icontains':query}))
        q_object=q_objects.pop()
        for name2 in q_objects:
            q_object|=name2
        query_set=query_set.filter(q_object)
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
