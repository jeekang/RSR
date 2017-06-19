from django.db import models
from datetime import date

class Person (models.Model):
    name = models.CharField(max_length= 200)
    school = models.CharField(max_length=200)
    school_level = models.CharField(max_length=30)
    major = models.CharField(max_length=100)
    graduation_date = models.DateField(default=date.today)
    language = models.CharField(max_length=200)
    skills = models.CharField(max_length=500)
    certificate = models.CharField(max_length=200)
    awards = models.CharField(max_length=200)
    conference = models.CharField(max_length=300)
    prior_company = models.CharField(max_length=100)
    year_of_experience = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    title = models.CharField(max_length=200)
    work_authorization = models.CharField(max_length=100)
    security_clearance = models.CharField(max_length=100)








