# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from RSR.models import Document
from RSR.forms import DocumentForm


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
