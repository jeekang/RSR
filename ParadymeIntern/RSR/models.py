# -*- coding: utf-8 -*-
import os

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from datetime import date, datetime
from django.db.models.signals import post_delete


import docx2txt

import os


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y%m%d')
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    operator = models.CharField(max_length=128)

    def __unicode__(self):
        return u'%s' %self.docfile

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))
        super(Document, self).delete(*args, **kwargs)



    wordstr = models.TextField()
	


class Person(models.Model):
    def get_absolute_url (self):
        return reverse('major_detail',  args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents = True, inclue_hidden = False):
            value = getattr(self, field.name, None)
            yield (field, value)

    CurrentEmployee = 'Employee'
    ProspectiveEmployee = 'Prospective'
    EmpChoices = ((CurrentEmployee,'Current Employee'),(ProspectiveEmployee,'Prospective Employee'))


    Name = models.CharField("Name", max_length = 50)
    Email = models.CharField("Email", max_length = 50)
    Address = models.CharField("Address", max_length = 50)
    ZipCode = models.IntegerField()
    State = models.CharField("State", max_length = 25)
    PhoneNumber = models.CharField("Phone", max_length = 50)
    Resume = models.FileField(upload_to = 'resumes')

    CreationDate = models.DateTimeField("Creation")
    LastUpdated = models.DateTimeField("Update",blank =True,null=True)
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL)
    Linkden = models.CharField("Linkden", max_length = 70)
    GitHun = models.CharField("GitHub", max_length = 70)
    TypeResume = models.CharField(max_length = 50,choices = EmpChoices,default = ProspectiveEmployee)

class OCR(models.Model):

    def get_absolute_url (self):
        return reverse('major_detail',  args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents = True, inclue_hidden = False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Resume = models.FileField(upload_to = 'PreOCR')


    CreationDate = models.DateTimeField("Creation")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL)
    NewPath = models.ForeignKey(Person,blank = True, null = True)


class Major(models.Model):

    def get_absolute_url (self):
        return reverse('major_detail',  args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents = True, inclue_hidden = False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Name", db_column='Name', max_length = 50)
    Dept = models.CharField("Department Name", db_column='Dept', max_length = 50)
    MajorMinor = models.CharField("Major/Minor", db_column='Major/Minor', max_length = 50)


class School(models.Model):

    def get_absolute_url (self):
        return reverse('School_detail',  args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents = True, inclue_hidden = False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("School Name", db_column='Name', max_length = 50)
    GradorUndergrad = models.CharField("Graduate or Undergraduate", db_column='GradorUndergrad', max_length = 50)


class Coursework(models.Model):

    def get_absolute_url (self):
        return reverse('Coursework_detail',  args=[str(self.id)])

    def __str__(self):
        return self.Name

    def __iter__(self):
        for field in self._meta.get_fields(include_parents = True, inclue_hidden = False):
            value = getattr(self, field.name, None)
            yield (field, value)

    Name = models.CharField("Coursework Name", db_column='Name', max_length = 50)
    Desc = models.CharField("Description", db_column='Desc', max_length = 50)


class Person_to_course(models.Model):
    CourseID = models.ForeignKey(Coursework, models.DO_NOTHING, db_column='CourseID')
    PersonID = models.ForeignKey(Person, models.DO_NOTHING, db_column='PersonID')

class Person_to_School(models.Model):
    GradDate = models.CharField("Grad Date", db_column = 'GradDate', max_length = 20)
    GPA = models.CharField("GPA", db_column = 'GPA', max_length = 20)
    CourseID = models.ForeignKey(Coursework, models.DO_NOTHING, db_column='CourseID')
    PersonID = models.ForeignKey(Person, models.DO_NOTHING, db_column='PersonID')
    SchoolID = models.ForeignKey(School, models.DO_NOTHING, db_column='SchoolID')
    MajorID = models.ForeignKey(Major, models.DO_NOTHING, db_column='MajorID')


##################### Certificate #####################
class Certificate(models.Model):
	def get_absolute_url(self):
		return reverse('Certificate_detail', args=[str(self.id)])

	def __str__(self):
	    return self.Name

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	Name = models.CharField("Name", db_column='Name', max_length=20)
	Description = models.CharField("Description", db_column='Description', max_length=30)

#################### Side Project ######################
class SideProject(models.Model):
	def get_absolute_url(self):
	    return reverse('SideProject_detail', args=[str(self.id)])

	def __str__(self):
		return self.ProjectName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	ProjectName = models.CharField("Project Name", db_column='ProjectName', max_length=20)
	ProjectDesc = models.CharField("Project Description", db_column='ProjectDesc', max_length=50)

#################### Skills ############################
class Skills(models.Model):
	def get_absolute_url(self):
		return reverse('Skills_detail', args=[str(self.id)])

	def __str__(self):
		return self.SkillsName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	SkillsName = models.CharField("Skills Name", db_column='SkillsName', max_length=20)

#################### Language Spoken ######################
class LanguageSpoken(models.Model):
	def get_absolute_url(self):
		return reverse('LanguageSpoken_detail', args=[str(self.id)])

	def __str__(self):
		return self.Language

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	Language = models.CharField("Language", db_column='Language', max_length=20)

#################### Clearence ######################
class Clearence(models.Model):
	def get_absolute_url(self):
		return reverse('Clearence_detail', args=[str(self.id)])

	def __str__(self):
		return self.ClearenceLevel

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	ClearenceLevel = models.CharField("Clearence Level", db_column='ClearenceLevel', primary_key=True, max_length=30)

#################### Person To Certificate ######################
class Person_Certificate(models.Model):

	PersonID = models.ForeignKey(Person, models.DO_NOTHING, db_column='PersonID')
	CertID = models.ForeignKey(Certificate, models.DO_NOTHING, db_column='CertID')

#################### Person To Side #############################
class Person_Side(models.Model):

	SideID = models.ForeignKey(SideProject, models.DO_NOTHING, db_column='SideID')
	PersonID = models.ForeignKey(Person, models.DO_NOTHING, db_column='PersonID')

#################### Person To Skills ###########################
class Person_Skills(models.Model):

	YearsOfExperience = models.CharField("Years Of Experience", db_column='YrsOfExp', max_length=3)
	SkillsID = models.ForeignKey(Skills, models.DO_NOTHING, db_column='SkillsID')
	PersonID = models.ForeignKey(Person, models.DO_NOTHING, db_column='PersonID')

#################### Person To Language #########################
class Person_Language(models.Model):

	PersonID = models.ForeignKey(Person, models.DO_NOTHING, db_column='PersonID')
	LangID = models.ForeignKey(LanguageSpoken, models.DO_NOTHING, db_column='LangID')

#################### Person To Clearence ########################
class Person_Clearence(models.Model):

	PersonID = models.ForeignKey(Person, models.DO_NOTHING, db_column='PersonID')
	ClearenceLevel = models.ForeignKey(Clearence, models.DO_NOTHING, db_column='ClearenceLevel')

class Company(models.Model):
	def get_absolute_url(self):
		return reverse('Company_detail', args=[str(self.id)])

	def __str__(self):
		return self.CompanyName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	CompanyName = models.CharField("Company Name", max_length=100)



class Awards(models.Model):

	def get_absolute_url(self):
		return reverse('award_detail', args=[str(self.id)])

	def __str__(self):
		return self.AwardName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	AwardName = models.CharField("Award Name", max_length=100)
	AwardDescriptioin = models.CharField("Award Description", max_length = 1000)




class Clubs_Hobbies(models.Model):

	def get_absolute_url(self):
		return reverse('clubs_hobbies_detail', args=[str(self.id)])

	def __str__(self):
   		return self.CHName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	CHName = models.CharField("Club and Hobby Name", max_length=100)
	CHDesc = models.CharField("Club and Hobby Description", max_length=100)

class Volunteering(models.Model):

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('volunteering_detail', args=[str(self.id)])

	def __str__(self):
   		return self.VolunName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	VounName = models.CharField("Volunteering Name", max_length=100)
	VolunDesc = models.CharField("Volunteering Description", max_length=1000)



# INTERMEDIARY TABLES

class Person_Company(models.Model):
	PersonID = models.ForeignKey(Person)
	CompanyName = models.ForeignKey(Company)
	Title = models.CharField("Title", max_length = 100, default = None)
	ExperienceOnJob = models.CharField("Experience on Job", max_length = 300, default = None)
	StartDate = models.DateField("Start Date", default=datetime.now().day)
	EndDate = models.DateField("End Date", default=datetime.now().day)

class Person_Awards(models.Model):
	PersonID = models.ForeignKey(Person)
	AwardName = models.ForeignKey(Awards)

class Person_Clubs_Hobbies(models.Model):
	PersonID = models.ForeignKey(Person)
	CHName = models.ForeignKey(Clubs_Hobbies)

class Person_Volunteering(models.Model):
	PersonID = models.ForeignKey(Person)
	VolunName = models.ForeignKey(Volunteering)


#tina pull request delete functions
#@receiver(models.signals.post_delete, sender=Document)
#def auto_delete_file_on_delete(sender, instance, **kwargs):

    #if instance.file:
        #if os.path.isfile(instance.file.path):
         #   os.remove(instance.file.path)
