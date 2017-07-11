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

from PIL import Image
from wand.image import Image as IMG
import pytesseract
import os


# UI/INGEST TEAM
def main(request):
    return render(request, 'main.html')

#OCR Team
def get_string(name):
    img=Image.open(name)
    utf8_text = pytesseract.image_to_string(img)
    utf8_text = str(utf8_text.encode('ascii', 'ignore'))
    return utf8_text


def uploaddoc(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            img=IMG(filename=newdoc.docfile.path,resolution=200)
            img.save(filename='temp.jpg')
            utf8_text = get_string('temp.jpg')
            os.remove('temp.jpg')
            print(utf8_text)
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


class detail(generic.DetailView):
    model = Person
    template_name = 'SearchExport/detail.html'


def export(request):
    return render(request, 'export.html')


# LINK ANALYSIS TEAM
def linkanalysis(request):
    return render(request, 'linkanalysis.html')
