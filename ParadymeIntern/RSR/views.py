
from .models import * 

# Create your views here.
#=======
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from RSR.models import Document
from RSR.forms import DocumentForm


def main(request):
    return render(request, 'main.html')

def uploaddoc(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return HttpResponseRedirect(reverse('uploaddoc'))
    else:
        form = DocumentForm()


    documents = Document.objects.all()


    return render(
        request,
        'index.html',
        {'documents': documents, 'form': form}
    )

def ocr (request):
    return render(request, 'ocr.html')

def parsing(request):
    return render(request, 'parsing.html')

def search (request):
    return render(request, 'search.html')

def user_acc_cont (request):
    return render(request, 'acc_cont.html')

def export(request):
    return render (request, 'export.html')

def linkanalysis(request):
    return render(request, 'linkanalysis.html')

