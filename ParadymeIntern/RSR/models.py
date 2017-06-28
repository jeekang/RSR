from django.db import models
import string

class Person (models.Model):
    name = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    school_level = models.CharField(max_length=30)
    major = models.CharField(max_length=100)
    gpa = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    graduation_year = models.IntegerField(default=1900)
    graduation_month = models.IntegerField(default=0)
    language = models.CharField(max_length=200)
    skills = models.CharField(max_length=500)
    certificate = models.CharField(max_length=500)
    awards = models.CharField(max_length=500)
    professional_development = models.CharField(max_length=500)
    prior_company = models.CharField(max_length=100)
    year_of_experience = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    title = models.CharField(max_length=200)
    work_authorization = models.CharField(max_length=100)
    security_clearance = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            field_name=field.get_attname()
            val=getattr(self, field_name)
            # Removing underscore and capitalizing the first word for each field name
            field_name=field_name.replace('_',' ')
            field_name=string.capwords(field_name)
            yield field_name+": "+str(val)



class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y%m%d')
