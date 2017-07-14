# -*- coding: utf-8 -*-
from .models import *
#import docx2txt

# Create your views here.
#=======
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.template import loader

from .models import *
from .models import Document
from .forms import DocumentForm
from .filters import PersonFilter
from django.db.models import Q

from django.forms import ModelForm

from .models import *
from .forms import DocumentForm

from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .filters import *
###Search #
from django.db.models import Q

###TESTING OCR
from PIL import Image
from wand.image import Image as IMG
import pytesseract
# import textract
###

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def main(request):
    return render(request, 'main.html')

def get_string(name):
    img=Image.open(name)
    utf8_text = pytesseract.image_to_string(img)
    utf8_text = str(utf8_text.encode('ascii', 'ignore'))
    return utf8_text


@login_required
def uploaddoc(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            temp_doc = Document(docfile=request.FILES['docfile'])

            #temp_doc.firstname = Document(docfile=request.POST.get('firstname'))
            #temp_doc.lastname = Document(docfile=request.POST.get('lastname'))
            #temp_doc.type = Document(docfile=request.POST.get('type'))
            temp_doc.firstname = request.POST['firstname']
            temp_doc.lastname = request.POST['lastname']
            temp_doc.type = request.POST['type']

            temp_doc.save()

            if ".doc" in temp_doc.docfile.path:
                print (temp_doc.docfile.path)
                temp_doc.docfile.wordstr = parse_word_file(temp_doc.docfile.path)
                print (temp_doc.docfile.wordstr)
                temp_doc.save(update_fields=['wordstr'])
            else:

                # temp_doc.docfile.wordstr = textract.process(temp_doc.docfile.path)
                path = os.path.join(settings.MEDIA_ROOT, temp_doc.docfile.name)
                # if len(temp_doc.docfile.wordstr) < 50:
                img=IMG(filename=path,resolution=200)
                # save in temp folder
                temp_path = os.path.join(settings.MEDIA_ROOT,'temp/temp')
                images=img.sequence
                for i in range(len(images)):
                    IMG(images[i]).save(filename=temp_path+str(i)+".jpg")
                for i in range(len(images)):
                    if i==0:
                        utf8_text = get_string(os.path.normpath(temp_path+str(i)+'.jpg'))
                        # delete from temp folder
                        os.remove(temp_path + str(i) + '.jpg')
                    else:
                        utf8_text+="\n\n"
                        utf8_text+=get_string(os.path.normpath(temp_path+str(i)+'.jpg'))
                        # delete from temp folder
                        os.remove(temp_path+str(i)+'.jpg')

                temp_doc.docfile.wordstr = utf8_text
                #endif - do not uncomment

                print (temp_doc.docfile.wordstr)
                temp_doc.save(update_fields=['wordstr'])
            return HttpResponseRedirect(reverse('RSR:uploaddoc'))
    else:
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request,'index.html',{'documents': documents, 'form': form})



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

@login_required
def ocr (request):

    return render(request, 'ocr.html')

@login_required
def parsing(request):
    return render(request, 'parsing.html')

@login_required
def search(request):
    query_set = Person.objects.all()
    query = request.GET.get("q")
    if query:
        query_set=query_set.filter(Name__icontains=query)
    # The filtered query_set is then put through more filters from django
    personFilter = PersonFilter(request.GET, query_set)
    return render(request, 'SearchExport/search.html', {'personFilter': personFilter})

@login_required
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



@login_required
def user_acc_cont (request):
    return render(request, 'acc_cont.html')

@login_required
def export(request):
    return render (request, 'export.html')

@login_required
def linkanalysis(request):
    return render(request, 'linkanalysis.html')

@login_required
def uploadlist (request):
   # documents = Document.objects.filter(firstname = Document.firstname).filter(lastname = Document.lastname).filter(type = Document.type).filter(docfile = Document.docfile)
    documents = UploadListFilter(request.GET,queryset = Document.objects.all())
    #documents = Document.objects.all()
    context ={'documents':documents}
    return render(request,'uploadlist.html',context)

def listdelete(request, template_name='uploadlist.html'):
    docId = request.POST.get('docfile', None)
    documents = get_object_or_404(Document, pk=docId)
    if request.method == 'POST':
        documents.delete()
        return HttpResponseRedirect(reverse('RSR:uploadlist'))

    return render(request, template_name, {'object': documents})


def parse_word_file(filepath):
	parsed_string = docx2txt.process(filepath)
	return parsed_string
