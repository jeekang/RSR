from django.db import models
import string
class School(models.Model):
    school = models.CharField(max_length=200)

    def __str__(self):
        return self.school

class School_level(models.Model):
    school_level = models.CharField(max_length=30)

    def __str__(self):
        return self.school_level

class Major(models.Model):
    major = models.CharField(max_length=100)

    def __str__(self):
        return self.major

class Graduation_Year(models.Model):
    graduation_year = models.IntegerField(default=1900)

    def __str__(self):
        return str(self.graduation_year)

class Graduation_Month(models.Model):
    graduation_month = models.CharField(max_length=20)

    def __str__(self):
        return self.graduation_month

class Work_Authorization(models.Model):
    work_authorization = models.CharField(max_length=50)

    def __str__(self):
        return self.work_authorization

class Security_Clearance(models.Model):
    security_clearance = models.CharField(max_length=100)

    def __str__(self):
        return self.security_clearance

class Person (models.Model):
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School)
    school_level = models.ForeignKey(School_level)
    major = models.ForeignKey(Major)
    gpa = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    graduation_year = models.ForeignKey(Graduation_Year)
    graduation_month = models.ForeignKey(Graduation_Month)
    language = models.CharField(max_length=200)
    skills = models.CharField(max_length=500)
    certificate = models.CharField(max_length=500)
    awards = models.CharField(max_length=500)
    professional_development = models.CharField(max_length=500)
    prior_company = models.CharField(max_length=100)
    year_of_experience = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    title = models.CharField(max_length=200)
    work_authorization = models.ForeignKey(Work_Authorization)
    security_clearance = models.ForeignKey(Security_Clearance)

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            field_name = field.get_attname()
            # In self._meta.fields for foreign key it returns field_name +"_id" so I just removed id so we get the value
            # of the field instead of id.
            if field_name.find('_id'):
                field_name = field_name.replace('_id', '')
            val = getattr(self, field_name)
            # Removing underscore and capitalizing the first word for each field name
            field_name = field_name.replace('_', ' ')
            field_name = string.capwords(field_name)
            if field_name == "Id":
                continue
<<<<<<< HEAD
            yield field_name+": "+str(val)
=======
            field_name = field_name.replace(' Id', '')
            yield field_name + ": " + str(val)
>>>>>>> a61840254f1fec4a351f16ae3b22f159e5d28780



class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y%m%d')
