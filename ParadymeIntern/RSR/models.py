# -*- coding: utf-8 -*-
import os

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from datetime import date, datetime
from django.dispatch import receiver
from django.db.models.signals import post_delete

import docx2txt
import string


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y%m%d')
    def __unicode__(self):
        return u'%s' %self.docfile

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))
        super(Document, self).delete(*args, **kwargs)

    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    uploaduser = models.CharField(max_length=128)
    wordstr = models.TextField()





class Person(models.Model):
    def get_absolute_url(self):
        return reverse('person_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        '''for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)'''
        for field in self._meta.fields:
            field_name = field.get_attname()
            field_name_1 = field.verbose_name
            # In self._meta.fields for foreign key it returns field_name +"_id" so I just removed id so we get the value
            # of the field instead of id.
            if field_name == "id":
                continue
            if field_name.find('_id') != -1:
                field_name = field_name.replace('_id', '')
            val = getattr(self, field_name)
            # Removing underscore and capitalizing the first word for each field name
            field_name = string.capwords(field_name)
            yield [field_name_1,str(val)]

    TYPERESUME_CHOICES = (('Employee', 'Employee'),
    ('Intern', 'Intern'),
    ('Prospective Employee', 'Prospective Employee'),
    ('Prospective Intern', 'Prospective Intern'),
)

    WORKAUTHORIZATION_CHOICES = (
        ('Citizenship', 'Citizenship'),
        ('Permanent Resident', 'Permanent Resident'),
        ('Visa', 'Visa')
    )

    Name = models.CharField(verbose_name = "Name", max_length = 50,default = "None")
    Email = models.CharField(verbose_name = "Email", max_length = 50,default = "None")
    Address = models.CharField(verbose_name = "Address", max_length = 50,default = "None")
    ZipCode = models.IntegerField(verbose_name = "Zip Code", default = "None")
    State = models.CharField(verbose_name = "State", max_length = 25,default = "None")
    PhoneNumber = models.CharField(verbose_name = "Phone", max_length = 50,default = "None")
    Resume = models.FileField(verbose_name = "Resume", upload_to = 'resumes', null = True) # null = True for testing purposes
    CreationDate = models.DateTimeField(verbose_name = "Created On",auto_now_add=True, blank=True)
    LastUpdated = models.DateTimeField(verbose_name = "Last Updated", blank = True, auto_now=True, null = True)
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "Created By",null = True) # null = True for testing purposes
    Linkedin = models.CharField(verbose_name = "LinkedIn", max_length = 70, default = "None")
    GitHub = models.CharField(verbose_name = "GitHub", max_length = 70, default = "None")
    TypeResume = models.CharField(verbose_name = "Type",max_length = 50, choices = TYPERESUME_CHOICES, default = 'Current Employee')
    WorkAuthorization = models.CharField(verbose_name = "Work Authorization", max_length=20, choices=WORKAUTHORIZATION_CHOICES, default ='Citizenship')
    Comments = models.CharField(max_length = 500, default = "Add Comment...")

class OCR(models.Model):
    def get_absolute_url(self):
        return reverse('major_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, inclue_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Resume = models.FileField(upload_to='PreOCR')
    CreationDate = models.DateTimeField("Creation")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL)
    NewPath = models.ForeignKey(Person, blank=True, null=True)


class Major(models.Model):
    Major_Choices = (('Major', 'Major'),
        ('Minor', 'Minor')
        )  
    def get_absolute_url(self):
        return reverse('major_detail', args=[str(self.id)])
    def __str__(self):
        return self.Name

    def __iter__(self):
        '''for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)'''
        for field in self._meta.fields:
            field_name = field.get_attname()
            field_name_1 = field.verbose_name
            # In self._meta.fields for foreign key it returns field_name +"_id" so I just removed id so we get the value
            # of the field instead of id.
            if field_name == "id":
                continue
            if field_name.find('_id') != -1:
                field_name = field_name.replace('_id', '')
            val = getattr(self, field_name)
            # Removing underscore and capitalizing the first word for each field name
            field_name = string.capwords(field_name)
            yield [field_name_1,str(val)]

    Name = models.CharField("Major", max_length=50,default = "None")
    Dept = models.CharField("Department", max_length=50,default = "None")
    MajorMinor = models.CharField("Major/Minor", max_length=50,choices = Major_Choices, default = "Major")


class School(models.Model):
    def get_absolute_url(self):
        return reverse('School_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, inclue_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    DEGREELEVEL_CHOICES = (
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate')
    )

    Name = models.CharField("School", max_length=50,default = "None")
    DegreeLevel = models.CharField("Degree Level", max_length=50, choices = DEGREELEVEL_CHOICES, default = 'Undergraduate')


class Coursework(models.Model):
    def get_absolute_url(self):
        return reverse('Coursework_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, inclue_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Coursework", max_length=50)



class ProfessionalDevelopment(models.Model):
    def get_absolute_url(self):
        return reverse('ProfessionalDevelopment_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Professional Development", max_length=20,default = "None")


class SideProject(models.Model):
    def get_absolute_url(self):
        return reverse('SideProject_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Project", max_length=20,default = "None")



class Skills(models.Model):
    def get_absolute_url(self):
        return reverse('Skills_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Skills", max_length=20,default = "None")


class LanguageSpoken(models.Model):
    def get_absolute_url(self):
        return reverse('LanguageSpoken_detail', args=[str(self.id)])

    def __str__(self):
        return self.Language

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Language = models.CharField("Language", max_length=20,default = "None")


class Clearance(models.Model):
    def get_absolute_url(self):
        return reverse('Clearance_detail', args=[str(self.id)])

    def __str__(self):
        return self.ClearanceLevel

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    ClearanceLevel = models.CharField("Clearance Level", primary_key=True, max_length=30,default = "None")


class Company(models.Model):
    def get_absolute_url(self):
        return reverse('Company_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Company Name", max_length=100,default = "None")


class Awards(models.Model):
    def get_absolute_url(self):
        return reverse('award_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Award Name", max_length=100,default = "None")


class Clubs_Hobbies(models.Model):
    def get_absolute_url(self):
        return reverse('clubs_hobbies_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Club and Hobby Name", max_length=100,default = "None")


class Volunteering(models.Model):
    def get_absolute_url(self):
        return reverse('volunteering_detail', args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents=True, include_hidden=False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Volunteering Name", max_length=100,default = "None")



######### INTERMEDIARY TABLES ##########

class PersonToCompany(models.Model):
    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    CompanyID = models.ForeignKey(Company,  on_delete=models.CASCADE)
    Title = models.CharField("Title", max_length=100, default="None")
    ExperienceOnJob = models.CharField("Experience on Job", max_length=300, default="None")
    StartDate = models.DateField("Start Date", default=datetime.now().day)
    EndDate = models.DateField("End Date", default=datetime.now().day)
    Desc = models.CharField("Company Description", max_length=1000, default="None")


class PersonToAwards(models.Model):

    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    AwardID = models.ForeignKey(Awards,  on_delete=models.CASCADE)
    Desc = models.CharField("Award Description", max_length=1000, default="None")


class PersonToClubs_Hobbies(models.Model):
    PersonID = models.ForeignKey(Person, related_name='persontoclubshobbies_set')
    CHID = models.ForeignKey(Clubs_Hobbies, related_name='persontoclubshobbies_set')
    Desc = models.CharField("Club and Hobby Description", max_length=100, default="None")


class PersonToVolunteering(models.Model):
    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    VolunID = models.ForeignKey(Volunteering,  on_delete=models.CASCADE)
    Desc = models.CharField("Volunteering Description", max_length=1000, default="None")


class PersonToProfessionalDevelopment(models.Model):
    def __str__(self):
        return self.PersonID.Name + ' - ' + self.ProfID.Name

    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    ProfID = models.ForeignKey(ProfessionalDevelopment,  on_delete=models.CASCADE)
    Desc = models.CharField("Professional Development Description", max_length=30, default="None")


class PersonToSide(models.Model):
    SideID = models.ForeignKey(SideProject, on_delete=models.CASCADE)
    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    Desc = models.CharField("Project Description", max_length=50, default="None")


class PersonToSkills(models.Model):

    def __str__(self):
        return self.PersonID.Name + ' - ' + self.SkillsID.Name
    YearsOfExperience = models.CharField("Years Of Experience", max_length=3)
    SkillsID = models.ForeignKey(Skills,  on_delete=models.CASCADE)
    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)


class PersonToLanguage(models.Model):
    def __str__(self):
        return self.PersonID.Name + ' - ' + self.LangID.Language

    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    LangID = models.ForeignKey(LanguageSpoken,  on_delete=models.CASCADE)


class PersonToClearance(models.Model):
    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    ClearanceLevel = models.ForeignKey(Clearance,  on_delete=models.CASCADE)


class PersonToCourse(models.Model):
    CourseID = models.ForeignKey(Coursework,  on_delete=models.CASCADE)
    Desc = models.CharField("Coursework Description", max_length=50,default = "None")
    PersonID = models.ForeignKey(Person, on_delete=models.CASCADE)


class PersonToSchool(models.Model):
    def __str__(self):
        return self.PersonID.Name + ' - ' + self.SchoolID.Name

    SchoolID = models.ForeignKey(School,  on_delete=models.CASCADE)
    GradDate = models.CharField("Graduation Date", max_length=20,default = "None")
    GPA = models.FloatField("GPA", max_length=20,default = "None")
    PersonID = models.ForeignKey(Person,  on_delete=models.CASCADE)
    MajorID = models.ForeignKey(Major,  on_delete=models.CASCADE)



# tina pull request delete functions
# @receiver(models.signals.post_delete, sender=Document)
# def auto_delete_file_on_delete(sender, instance, **kwargs):

# if instance.file:
# if os.path.isfile(instance.file.path):
#   os.remove(instance.file.path)
