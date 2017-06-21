from django.db import models
from datetime import date

school_choices = (
    ('University of Maryland', 'University of Maryland'),
    ('Ohio State University', 'Ohio State University'),
    ('University of Indiana', 'University of Indiana'),
)

school_level_choices = (
    ('Undergraduate', 'Undergraduate'),
    ('Graduate', 'Graduate'),
    ('PhD', 'PhD'),
)

class Person (models.Model):
    name = models.CharField(max_length=200)
    school = models.CharField(max_length=200, choices=school_choices)
    school_level = models.CharField(max_length=30, choices=school_level_choices)
    major = models.CharField(max_length=100)
    graduation_date = models.DateField(default=date.today)
    language = models.CharField(max_length=200)
    skills = models.CharField(max_length=500)
    certificate = models.TextField()
    awards = models.TextField()
    conference = models.TextField()
    prior_company = models.CharField(max_length=100)
    year_of_experience = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    title = models.CharField(max_length=200)
    work_authorization = models.CharField(max_length=100)
    security_clearance = models.CharField(max_length=100)

    def __str__(self):
        return self.name








