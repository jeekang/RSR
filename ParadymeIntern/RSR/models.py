from django.db import models

class Person (models.Model):
    name = models.CharField(max_length= 200)
    school = models.CharField(max_length=200)
    school_level = models.CharField(max_length=30)
    major = models.CharField(max_length=100)
    graduation_date = models.DateField
    language = models.CharField(max_length=200)
    skills = models.CharField(max_length=500)
    certificate = models.CharField(max_length=200)
    awards = models.CharField(max_length=200)
    conference = models.CharField(max_length=300)
    prior_company = models.CharField(max_length=100)
    year_of_experience = models.DecimalField
    title = models.CharField(max_length=200)
    work_authorization = models.CharField(max_length=100)
    security_clearance = models.CharField(max_length=100)







