# -*- coding: utf-8 -*-
from .models import *
import docx2txt

# Create your views here.
#=======
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

from RSR.models import *
from RSR.forms import DocumentForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .filters import *
###Search #
from django.db.models import Q
from RSR.persondetails import Detail
from RSR.persondetails2 import Detail2

### json Parsing ##
import json

###TESTING OCR
#from PIL import Image
#from wand.image import Image as IMG
#import pytesseract
#import textract
### 



def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def main(request):
    return render(request, 'main.html')

#def get_string(name):
#    img=Image.open(name)
#    utf8_text = pytesseract.image_to_string(img)
#    utf8_text = str(utf8_text.encode('ascii', 'ignore'))
#    return utf8_text


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
            temp_doc.uploaduser = request.user.username

            temp_doc.save()

            if ".doc" in temp_doc.docfile.path:
                print (temp_doc.docfile.path)
                temp_doc.docfile.wordstr = parse_word_file(temp_doc.docfile.path)
                print (temp_doc.docfile.wordstr)
                temp_doc.save(update_fields=['wordstr'])
            
            #else:

            #    temp_doc.docfile.wordstr = textract.process(temp_doc.docfile.path)
                
            #    if len(temp_doc.docfile.wordstr) < 50:
            #       img=IMG(filename=temp_doc.docfile.path,resolution=200)
                    
            #        img.save(filename='temp.jpg')
            #        utf8_text = get_string('temp.jpg')
            #        os.remove('temp.jpg')
                    
            #        print (utf8_text)
            #        temp_doc.docfile.wordstr = utf8_text
            #        temp_doc.save(update_fields=['wordstr'])

            #    print (temp_doc.docfile.wordstr)
            #    temp_doc.save(update_fields=['wordstr'])


            #json testing#
            #check for json file, wont be needed as parsing will return json#
            if ".json" in temp_doc.docfile.path:
                #either load json, or recieve json file
                js = json.load(open(temp_doc.docfile.path))
                #iterate through json file

                #initialize person out side of for loop/if statements so we can use it later
                person = Person(Name="temp")
                for label in js:
                    
                    #Checking Labels to see which table to create
                    if label == "person":
                        for key in js[label]:
                            if key == "name":
                                person.Name = js[label][key]
                            elif key == "email":
                                person.Email = js[label][key]
                            elif key == "address":
                                person.Address = js[label][key]
                            elif key == "zipcode":
                                person.ZipCode = js[label][key]
                            elif key == "state":
                                person.State = js[label][key]
                            elif key == "phone":
                                person.PhoneNumber = js[label][key]
                            elif key == "linkedin":
                                person.Linkedin = js[label][key]
                            elif key == "github":
                                person.GitHub = js[label][key]
                        person.Resume = temp_doc.docfile
                        person.save()

                    if label == "skills":
                        for key in js[label]:
                            #check to see if skill exists
                            query_set=Skills.objects.all()
                            query_set=query_set.filter(Name__icontains=js[label][key])
                            #if skill does not exist create skill
                            if not query_set:
                                query_set = Skills(Name = js[label][key])
                                query_set.save()
                            #if skill does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            skill_to_person = PersonToSkills(SkillsID = query_set, PersonID = person)
                            skill_to_person.save()



            return HttpResponseRedirect(reverse('RSR:uploaddoc'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    return render(request,'index.html',{'documents': documents, 'form': form})


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
    person = get_object_or_404(Person, pk=pk)
    related_obj_list=Detail(person)

    detail_dic = Detail2(person)
    School = detail_dic['PersonToSchool']
    Course = detail_dic['PersonToCourse']
    Pro = detail_dic['PersonToProfessionalDevelopment']
    Side = detail_dic['PersonToSide']
    Skills = detail_dic['PersonToSkills']
    Language = detail_dic['PersonToLanguage']
    Clearance = detail_dic['PersonToClearance']
    Company = detail_dic['PersonToCompany']
    Clubs = detail_dic['PersonToClubs_Hobbies']
    Volunteer = detail_dic['PersonToVolunteering']
    context = { 
                'person':person,
                'list': related_obj_list,
                'school':School,
                'course':Course,
                'pro':Pro,
                'side':Side,
                'skills':Skills,
                'language':Language,
                'clearance':Clearance,
                'company':Company,
                'clubs':Clubs,
                'volunteer':Volunteer,
                }

    return render(request, 'SearchExport/detail.html', context)





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

