# -*- coding: utf-8 -*-
from .models import *
import docx2txt
from django.utils import timezone

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
from RSR.forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .filters import *
###Search #
from django.db.models import Q
from RSR.persondetails import Detail
from RSR.persondetails2 import Detail2
from django.views.generic.edit import UpdateView
from dal import autocomplete


### json Parsing ##
import json

###TESTING OCR

from PIL import Image
from wand.image import Image as IMG
import pytesseract
# import textract

### Limit group###

from django.contrib.auth.decorators import user_passes_test



@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())

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
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def uploaddoc(request):
    # Handle file upload


    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #### PARSING TEAM = AT THE END OF THE NEXT LINES, USE
            #### temp_doc.wordstr TO GRAB STRING ####


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
                temp_doc.wordstr = parse_word_file(temp_doc.docfile.path)
                print (temp_doc.wordstr)
                temp_doc.save(update_fields=['wordstr'])

            ### UNCOMMENT THESE LINES FOR MAC/LINUX USERS: OCR/TEXTRACT

            else:

                # temp_doc.wordstr = textract.process(temp_doc.docfile.path)

                # if len(temp_doc.wordstr) < 50:
                img=IMG(filename=temp_doc.docfile.path,resolution=200)

                img.save(filename='temp.jpg')
                utf8_text = get_string('temp.jpg')
                os.remove('temp.jpg')

                print (utf8_text)
                temp_doc.wordstr = utf8_text
                temp_doc.save(update_fields=['wordstr'])

                print (temp_doc.wordstr)
                temp_doc.save(update_fields=['wordstr'])

            '''
            ============ PARSING TEAM =====================
            FROM HERE YOU CAN CALL temp_doc.wordstr HERE TO GRAB STRING

            ===============================================
            '''
            ###



            #json testing#
            #check for json file, wont be needed as parsing will return json#


            #========== PARSING TEAM JSON =========== #
            ## GET RID OF THIS LINE BELOW
            ## replace with below line:  (just so we dont have to redo indents)
            #if True:
            # ======================================#


            if ".json" in temp_doc.docfile.path:



                #either load json, or recieve json file

                ### ===================== ######
                #PARSING, REPLACE temp_doc.docfile.path with the json path!!
                ### ====================== ######
                js = json.load(open(temp_doc.docfile.path))


                #iterate through json file

                #initialize person out side of for loop/if statements so we can use it later
                p_name = temp_doc.firstname + " " + temp_doc.lastname
                person = Person(Name=p_name)
                for label in js:

                    #Checking Labels to see which table to create
                    if label == "person":
                        for key in js[label]:
                            #if key == "name":
                            #    person.Name = js[label][key]
                            if key == "email":
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
                        person.TypeResume = temp_doc.type
                        person.save()


                    elif label == "skills":
                        for key in js[label]:
                            #check to see if skill exists
                            query_set=Skills.objects.all()
                            query_set=query_set.filter(Name=key["skill"])
                            #if skill does not exist create skill
                            if not query_set:
                                query_set = Skills(Name = key["skill"])
                                query_set.save()
                            #if skill does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            skill_to_person = PersonToSkills(SkillsID = query_set, PersonID = person,YearsOfExperience = key["YearsOfExperience"])
                            skill_to_person.save()

                    elif label == "work":
                        for key in js[label]:
                            #check to see if company exists
                            query_set=Company.objects.all()
                            query_set=query_set.filter(Name=key["company"])
                            #if company does not exist create skill
                            if not query_set:
                                query_set = Company(Name = key["company"])
                                query_set.save()
                            #if company does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            #intermediary table stuff
                            company_to_person = PersonToCompany(CompanyID = query_set, PersonID = person,
                                Title = key["title"],
                                ExperienceOnJob = key["experience"],
                                StartDate = key["startDate"],
                                EndDate = key["endDate"],
                                Desc = key["summary"])
                            company_to_person.save()

                    elif label == "education":
                        for key in js[label]:
                            #check to see if School exists
                            query_set=School.objects.all()
                            query_set=query_set.filter(Name=key["school"]["name"]).filter(DegreeLevel = key["school"]["degreeLevel"])
                            #if School does not exist create skill
                            if not query_set:
                                query_set = School(Name = key["school"]["name"], DegreeLevel = key["school"]["degreeLevel"])
                                query_set.save()
                            #if School does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]

                            # NOW DO MAJOR
                            query_set_1=Major.objects.all()
                            query_set_1=query_set_1.filter(Name=key["major"]["major"]).filter(Dept__icontains = key["major"]["dept"]).filter(MajorMinor__icontains = key["major"]["major/minor"])
                            if not query_set_1:
                                query_set_1 = Major(Name = key["major"]["major"], Dept = key["major"]["dept"], MajorMinor = key["major"]["major/minor"])
                                query_set_1.save()
                            #if School does exist, grab first match from queryset
                            else:
                                query_set_1 = query_set_1[0]

                            #intermediary table stuff
                            ed_to_person = PersonToSchool(SchoolID = query_set, PersonID = person, MajorID = query_set_1,
                                GPA = key["GPA"],
                                GradDate = key["gradDate"])
                            ed_to_person.save()


                    elif label == "sideprojects":
                        for key in js[label]:
                            #check to see if project exists
                            query_set=SideProject.objects.all()
                            query_set=query_set.filter(Name=key["name"])
                            #if project does not exist create project
                            if not query_set:
                                query_set = SideProject(Name = key["name"])
                                query_set.save()
                            #if project does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            #intermediary table stuff
                            project_to_person = PersonToSide(SideID = query_set, PersonID = person, Desc = key["description"])
                            project_to_person.save()

                    elif label == "award":
                        for key in js[label]:
                            #check to see if Award exists
                            query_set=Awards.objects.all()
                            query_set=query_set.filter(Name=key["name"])
                            #if Award does not exist create Award
                            if not query_set:
                                query_set = Awards(Name = key["name"])
                                query_set.save()
                            #if Award does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            #intermediary table stuff
                            awards_to_person = PersonToAwards(AwardID = query_set, PersonID = person, Desc = key["description"])
                            awards_to_person.save()

                    elif label == "clearance":
                        query_set = Clearance.objects.all()
                        query_set = query_set.filter(ClearanceLevel = js[label]["level"])
                        if not query_set:
                            query_set = Clearance(ClearanceLevel=js[label]["level"])
                            query_set.save()
                        else:
                            query_set = query_set[0]
                        cl_to_person = PersonToClearance(PersonID=person, ClearanceLevel = query_set)
                        cl_to_person.save()

                    elif label == "languages":
                        for key in js[label]:
                            # check to see if language exists
                            query_set = LanguageSpoken.objects.all()
                            query_set = query_set.filter(Language=key["language"])
                            # if language does not exist create language
                            if not query_set:
                                query_set = LanguageSpoken(Language=key["language"])
                                query_set.save()
                            # if language does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            # intermediary table stuff
                            language_to_person = PersonToLanguage(LangID=query_set, PersonID=person)
                            language_to_person.save()

                    elif label == "clubs":
                        for key in js[label]:
                            # check to see if club exists
                            query_set = Clubs_Hobbies.objects.all()
                            query_set = query_set.filter(Name=key["name"])
                            # if club does not exist create club
                            if not query_set:
                                query_set = Clubs_Hobbies(Name=key["name"])
                                query_set.save()
                            # if club does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            # intermediary table stuff
                            club_to_person = PersonToClubs_Hobbies(CHID=query_set, PersonID=person, Desc=key["description"])
                            club_to_person.save()

                    elif label == "volunteering":
                        for key in js[label]:
                            # check to see if volunteer exists
                            query_set = Volunteering.objects.all()
                            query_set = query_set.filter(Name=key["name"])
                            # if volunteer does not exist create volunteer
                            if not query_set:
                                query_set = Volunteering(Name=key["name"])
                                query_set.save()
                            # if volunteer does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            # intermediary table stuff
                            volunteer_to_person = PersonToVolunteering(VolunID=query_set, PersonID=person, Desc=key["description"])
                            volunteer_to_person.save()

                    elif label == "course":
                        for key in js[label]:
                            # check to see if course exists
                            query_set = Coursework.objects.all()
                            query_set = query_set.filter(Name=key["name"])
                            # if course does not exist create course
                            if not query_set:
                                query_set = Coursework(Name=key["name"])
                                query_set.save()
                            # if course does exist, grab first match from queryset
                            else:
                                query_set = query_set[0]
                            # intermediary table stuff
                            course_to_person = PersonToCourse(CourseID=query_set, PersonID=person,Desc=key["description"])
                            course_to_person.save()


            return HttpResponseRedirect(reverse('RSR:uploaddoc'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    return render(request,'index.html',{'documents': documents, 'form': form})

#edit function
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def person_edit(request, person_id):
	instance = get_object_or_404(Person, id=person_id)
	form = PersonForm(request.POST or None, instance=instance)


	if form.is_valid():
		form.save()

		return HttpResponseRedirect(reverse('RSR:detail', args=[instance.pk]))
	context = {
		'form' : form,
		'pk' : person_id,
		'person':instance
	}
	return render(request, 'person_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def skill_edit(request, skill_id):
    instance = get_object_or_404(PersonToSkills, id=skill_id)
    form = PersontoSkillForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()

        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))
    context = {
        'form': form,
        'pk':skill_id,
        'person': instance
    }
    return render(request, 'skill_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def company_edit(request, company_id):
    instance = get_object_or_404(PersonToCompany, id=company_id)
    form = PersontoCompanyForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':company_id,
        'person': instance
    }
    return render(request, 'company_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def school_edit(request, school_id):
    instance = get_object_or_404(PersonToSchool, id=school_id)
    form = PersontoSchoolForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':school_id,
        'person': instance
    }
    return render(request, 'school_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def course_edit(request, course_id):
    instance = get_object_or_404(PersonToCourse, id=course_id)
    form = PersontoCourseForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':course_id,
        'person': instance
    }
    return render(request, 'course_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def language_edit(request, language_id):
    instance = get_object_or_404(PersonToLanguage, id=language_id)
    form = PersontoLanguageForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':language_id,
        'person': instance
    }
    return render(request, 'language_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def sidepro_edit(request, sidepro_id):
    instance = get_object_or_404(PersonToSide, id=sidepro_id)
    form = PersontoSideForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':sidepro_id,
        'person': instance
    }
    return render(request, 'sidepro_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def award_edit(request, award_id):
    instance = get_object_or_404(PersonToAwards, id=award_id)
    form = PersontoAwardForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':award_id,
        'person': instance
    }
    return render(request, 'award_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def club_edit(request, club_id):
    instance = get_object_or_404(PersonToClubs_Hobbies, id=club_id)
    form = PersontoClubForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':club_id,
        'person': instance
    }
    return render(request, 'club_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def volunteer_edit(request, volunteer_id):
    instance = get_object_or_404(PersonToVolunteering, id=volunteer_id)
    form = PersontoVolunteeringForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':volunteer_id,
        'person': instance
    }
    return render(request, 'volunteer_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def professional_edit(request,pro_id):
    instance = get_object_or_404(PersonToProfessionalDevelopment, id=pro_id)
    form = PersontoProfessionalForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':pro_id,
        'person': instance
    }
    return render(request, 'professional_update_form.html', context)

def clearance_edit(request,clearance_id):
    instance = get_object_or_404(PersonToClearance, id=clearance_id)
    form = PersontoClearanceForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':clearance_id,
        'person': instance
    }
    return render(request, 'clearance_update_form.html', context)

#end edit

##########delete##############

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def skill_delete(request,pk,template_name='skill_update_form.html'):
    skills = get_object_or_404(PersonToSkills, pk=pk)
    if request.method == 'POST':
        skills.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[skills.PersonID.pk]))
    return render(request, template_name, {'object': skills})



@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def company_delete(request,pk,template_name='detail.html'):
    company = get_object_or_404(PersonToCompany, pk=pk)
    if request.method == 'POST':
        company.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[company.PersonID.pk]))
    return render(request, template_name, {'object': company})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def school_delete(request,pk,template_name='detail.html'):
    school = get_object_or_404(PersonToSchool, pk=pk)
    if request.method == 'POST':
        school.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[school.PersonID.pk]))
    return render(request, template_name, {'object': school})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def course_delete(request,pk,template_name='detail.html'):
    course = get_object_or_404(PersonToCourse, pk=pk)
    if request.method == 'POST':
        course.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[course.PersonID.pk]))
    return render(request, template_name, {'object': course})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def language_delete(request,pk,template_name='detail.html'):
    language = get_object_or_404(PersonToLanguage, pk=pk)
    if request.method == 'POST':
        language.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[language.PersonID.pk]))
    return render(request, template_name, {'object': language})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def sidepro_delete(request,pk,template_name='detail.html'):
    sidepro = get_object_or_404(PersonToSide, pk=pk)
    if request.method == 'POST':
        sidepro.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[sidepro.PersonID.pk]))
    return render(request, template_name, {'object': sidepro})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def award_delete(request,pk,template_name='detail.html'):
    award = get_object_or_404(PersonToAwards, pk=pk)
    if request.method == 'POST':
        award.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[award.PersonID.pk]))
    return render(request, template_name, {'object': award})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def club_delete(request,pk,template_name='detail.html'):
    club = get_object_or_404(PersonToClubs_Hobbies, pk=pk)
    if request.method == 'POST':
        club.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[club.PersonID.pk]))
    return render(request, template_name, {'object': club})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def volunteer_delete(request,pk,template_name='detail.html'):
    volunteer = get_object_or_404(PersonToVolunteering, pk=pk)
    if request.method == 'POST':
        volunteer.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[volunteer.PersonID.pk]))
    return render(request, template_name, {'object': volunteer})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def professional_delete(request,pk,template_name='detail.html'):
    professional = get_object_or_404(PersonToProfessionalDevelopment, pk=pk)
    if request.method == 'POST':
        professional.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[professional.PersonID.pk]))
    return render(request, template_name, {'object': professional})

#########end delete###########





@login_required
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def detail(request,pk):
       # Get the current person object using pk or id
    person = get_object_or_404(Person, pk=pk)
    related_obj_list=Detail(person)

    detail_dic = Detail2(person)
    School_Detail = detail_dic['PersonToSchool']
    print(School_Detail)
    Course_Detail = detail_dic['PersonToCourse']
    Pro = detail_dic['PersonToProfessionalDevelopment']
    Side = detail_dic['PersonToSide']
    Skills_Detail = detail_dic['PersonToSkills']
    Language = detail_dic['PersonToLanguage']
    Clearance = detail_dic['PersonToClearance']
    Company_Detail = detail_dic['PersonToCompany']
    Clubs = detail_dic['PersonToClubs_Hobbies']
    Volunteer = detail_dic['PersonToVolunteering']
    Award = detail_dic['PersonToAwards']

    form = CommentsForm(request.POST or None, instance=person)


    if form.is_valid():
        form.save()

        return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))


    #add Skill
    skillform = SkillForm(request.POST)
    persontoskill = NewPersontoSkillForm(request.POST)
    if skillform.is_valid() and not skillform.cleaned_data['Name'] == "":
        skillform.save(commit=False)
        query_set = Skills.objects.all()


        if not query_set.filter(Name=skillform.cleaned_data['Name']):
            skillform.save()
            query_set = query_set.filter(Name=skillform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=skillform.cleaned_data['Name'])[0]
        if persontoskill.is_valid():
            print(persontoskill.cleaned_data['YearsOfExperience'])
            persontoskill_temp = persontoskill.save(commit=False)
            persontoskill_temp.SkillsID = query_set

            persontoskill_temp.PersonID = person

            persontoskill_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add skill

     #add Company
    companyform = CompanyForm(request.POST)
    persontocompany = NewPersontoCompanyForm(request.POST)
    if companyform.is_valid() and not companyform.cleaned_data['Name'] == "":
        companyform.save(commit=False)
        query_set = Company.objects.all()


        if not query_set.filter(Name=companyform.cleaned_data['Name']):
            companyform.save()
            query_set = query_set.filter(Name=companyform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=companyform.cleaned_data['Name'])[0]
        if persontocompany.is_valid():
            persontocompany_temp = persontocompany.save(commit=False)
            persontocompany_temp.CompanyID = query_set

            persontocompany_temp.PersonID = person

            persontocompany_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add company

      #add school
    majorform = NewMajorForm(prefix = "majorform")
    schoolform = NewSchoolForm(prefix = "schoolform")

    majorform = NewMajorForm(request.POST, prefix = "majorform")
    schoolform = NewSchoolForm(request.POST, prefix = "schoolform")
    persontoschool  = NewPersontoSchoolForm(request.POST)

    if schoolform.is_valid() and not schoolform.cleaned_data['Name'] == "":
        print(1)
        schoolform.save(commit=False)
        query_set = School.objects.all()


        if not query_set.filter(Name=schoolform.cleaned_data['Name']):
            schoolform.save()
            query_set = query_set.filter(Name=schoolform.cleaned_data['Name'])[0]
            print(query_set)
        else:
            query_set = query_set.filter(Name=schoolform.cleaned_data['Name'])[0]
            print(query_set)
        if majorform.is_valid():
            majorform.save(commit=False)
            query_set1 = Major.objects.all()


            if not query_set1.filter(Name=majorform.cleaned_data['Name'],MajorMinor = majorform.cleaned_data['MajorMinor']):
                majorform.save()
                query_set1 = query_set1.filter(Name=majorform.cleaned_data['Name'],MajorMinor = majorform.cleaned_data['MajorMinor'])[0]
                print(query_set1)
            else:
                query_set1 = query_set1.filter(Name=majorform.cleaned_data['Name'],MajorMinor = majorform.cleaned_data['MajorMinor'])[0]
                print(query_set1)

            if persontoschool.is_valid():
                persontoschool_temp = persontoschool.save(commit=False)
                print (12)
                persontoschool_temp.MajorID = query_set1
                persontoschool_temp.SchoolID = query_set

                persontoschool_temp.PersonID = person

                persontoschool_temp.save()
                return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add school
     #add Course
    courseform = CourseForm(prefix = "courseform")
    courseform = CourseForm(request.POST, prefix = "courseform")
    persontocourse = NewPersontoCourseForm(request.POST)
    if courseform.is_valid() and not courseform.cleaned_data['Name'] == "":
        print ("how1")
        courseform.save(commit=False)
        query_set = Coursework.objects.all()


        if not query_set.filter(Name=courseform.cleaned_data['Name']):
            courseform.save()
            query_set = query_set.filter(Name=courseform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=courseform.cleaned_data['Name'])[0]
        if persontocourse.is_valid():
            print ("how")
            persontocourse_temp = persontocourse.save(commit=False)
            persontocourse_temp.CourseID = query_set

            persontocourse_temp.PersonID = person

            persontocourse_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add course
    #add Lang
    langform = LanguageForm(prefix = "langform")
    langform = LanguageForm(request.POST, prefix = "langform")
    if langform.is_valid() and not langform.cleaned_data['Language'] == "":
        langform.save(commit=False)
        query_set = LanguageSpoken.objects.all()


        if not query_set.filter(Language=langform.cleaned_data['Language']):
            langform.save()
            query_set = query_set.filter(Language=langform.cleaned_data['Language'])[0]

        else:
            query_set = query_set.filter(Language=langform.cleaned_data['Name'])[0]
        language_to_person = PersonToLanguage(LangID=query_set, PersonID=person)
        language_to_person.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add Lang

        #add Side Project
    sideform = SideForm(prefix = "sideform")
    sideform = SideForm(request.POST, prefix = "sideform")
    persontoside = NewPersontoSideForm(request.POST)
    if sideform.is_valid() and not sideform.cleaned_data['Name'] == "":
        sideform.save(commit=False)
        query_set = SideProject.objects.all()


        if not query_set.filter(Name=sideform.cleaned_data['Name']):
            sideform.save()
            query_set = query_set.filter(Name=sideform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=sideform.cleaned_data['Name'])[0]
        if persontoside.is_valid():
            persontoside_temp = persontoside.save(commit=False)
            persontoside_temp.SideID = query_set

            persontoside_temp.PersonID = person

            persontoside_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add Project
    #add Award
    awardform = AwardForm(prefix = "awardform")
    awardform = AwardForm(request.POST, prefix = "awardform")
    persontoaward = NewPersontoAwardForm(request.POST)
    if awardform.is_valid() and not awardform.cleaned_data['Name'] == "":
        awardform.save(commit=False)
        query_set = Awards.objects.all()


        if not query_set.filter(Name=awardform.cleaned_data['Name']):
            awardform.save()
            query_set = query_set.filter(Name=awardform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=awardform.cleaned_data['Name'])[0]
        if persontoaward.is_valid():
            persontoaward_temp = persontoaward.save(commit=False)
            persontoaward_temp.AwardID = query_set

            persontoaward_temp.PersonID = person

            persontoaward_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add award

    #add Club
    clubform = ClubForm(prefix = "clubform")
    clubform = ClubForm(request.POST, prefix = "clubform")
    persontoclub = NewPersontoClubForm(request.POST)
    if clubform.is_valid() and not clubform.cleaned_data['Name'] == "":
        clubform.save(commit=False)
        query_set = Clubs_Hobbies.objects.all()


        if not query_set.filter(Name=clubform.cleaned_data['Name']):
            clubform.save()
            query_set = query_set.filter(Name=clubform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=clubform.cleaned_data['Name'])[0]
        if persontoclub.is_valid():
            persontoclub_temp = persontoclub.save(commit=False)
            persontoclub_temp.CHID = query_set

            persontoclub_temp.PersonID = person

            persontoclub_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add club


     #add volunteer
    volunteerform = VolunteeringForm(prefix = "volunteerform")
    volunteerform = VolunteeringForm(request.POST, prefix = "volunteerform")
    persontovolunteer = NewPersontoVolunteerForm(request.POST)
    if volunteerform.is_valid() and not volunteerform.cleaned_data['Name'] == "":
        volunteerform.save(commit=False)
        query_set = Volunteering.objects.all()


        if not query_set.filter(Name=volunteerform.cleaned_data['Name']):
            volunteerform.save()
            query_set = query_set.filter(Name=volunteerform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=volunteerform.cleaned_data['Name'])[0]
        if persontovolunteer.is_valid():
            persontovolunteer_temp = persontovolunteer.save(commit=False)
            persontovolunteer_temp.VolunID = query_set

            persontovolunteer_temp.PersonID = person

            persontovolunteer_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add volunteer

     #add Professional
    professionalform = ProfessionalForm(prefix = "professionalform")
    professionalform = ProfessionalForm(request.POST, prefix = "professionalform")
    persontoprofessional = NewPersontoProfessionalForm(request.POST)
    if professionalform.is_valid() and not professionalform.cleaned_data['Name'] == "":
        professionalform.save(commit=False)
        query_set = ProfessionalDevelopment.objects.all()


        if not query_set.filter(Name=professionalform.cleaned_data['Name']):
            professionalform.save()
            query_set = query_set.filter(Name=professionalform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=professionalform.cleaned_data['Name'])[0]
        if persontoprofessional.is_valid():
            persontoprofessional_temp = persontoprofessional.save(commit=False)
            persontoprofessional_temp.ProfID = query_set

            persontoprofessional_temp.PersonID = person

            persontoprofessional_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add club
    context = {
                'form' : form,
                'skillform': skillform,
                'majorform':majorform,
                'schoolform':schoolform,
                'persontoschool':persontoschool,
                'companyform':companyform,
                'courseform':courseform,
                'persontocourse':persontocourse,
                'persontocompany':persontocompany,
                'persontoskill':persontoskill,
                'person':person,
                'list': related_obj_list,
                'school':School_Detail,
                'course':Course_Detail,
                'pro':Pro,
                'professionalform':professionalform,
                'persontoprofessional':persontoprofessional,
                'side':Side,
                'sideform':sideform,
                'persontoside':persontoside,
                'skills':Skills_Detail,
                'language':Language,
                'langform':langform,
                'clearance':Clearance,
                'company':Company_Detail,
                'clubs':Clubs,
                'clubform':clubform,
                'persontoclub':persontoclub,
                'volunteer':Volunteer,
                'volunteerform':volunteerform,
                'persontovolunteer':persontovolunteer,
                'award':Award,
                'awardform':awardform,
                'persontoaward':persontoaward,
                }

    return render(request, 'SearchExport/detail.html', context)




@login_required
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def uploadlist (request):
   # documents = Document.objects.filter(firstname = Document.firstname).filter(lastname = Document.lastname).filter(type = Document.type).filter(docfile = Document.docfile)
    document = Document.objects.all()
    documents = UploadListFilter(request.GET,queryset = document)

    context ={'documents':documents}
    return render(request,'uploadlist.html',context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def listdelete(request, template_name='uploadlist.html'):
    docId = request.POST.get('docfile', None)
    documents = get_object_or_404(Document, pk=docId)
    if request.method == 'POST':


        documents.delete()
        return HttpResponseRedirect(reverse('RSR:uploadlist'))

    return render(request, template_name, {'object': documents})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def parse_word_file(filepath):
	parsed_string = docx2txt.process(filepath)
	return parsed_string



# SEARCH/EXPORT TEAM
@login_required
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
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

#OCR's Search. REGEX ON RESUME TEXT

def OCRSearch(request):
    doc_objects = Document.objects.all()
    search_item = str(request.GET.get('search'))
    print(search_item)
    results=[]
    for document in doc_objects:
        print(document.wordstr)
        wordstr = str(document.wordstr)
        if search_item.lower() in wordstr.lower():
            print(document.wordstr)
            results.append(document)
    context = {'results': results}

    return render(request, 'OCRSearch.html', context)
