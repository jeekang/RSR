from django.db import models
import string

school_choices = (
    ('University of Maryland', 'University of Maryland'),
    ('Ohio State University', 'Ohio State University'),
    ('Indiana University', 'Indiana University'),
)

school_level_choices = (
    ('Undergraduate', 'Undergraduate'),
    ('Graduate', 'Graduate'),
)

major_choices = (
    ('Accounting', 'Accounting'),
    ('Finance', 'Finance'),
    ('Information Systems', 'Information Systems'),
    ('Marketing', 'Marketing'),
    ('Management', 'Management'),
    ('Computer Science', 'Computer Science'),
    ('Supply Chain Mgmt', 'Supply Chain Mgmt'),
)

work_authorization_choices = (
    ('Citizenship', 'Citizenship'),
    ('Permanent Resident', 'Permanent Resident'),
    ('Visa', 'Visa'),
)

security_clearance_choices = (
    ('Top Secret', 'Top Secret'),
    ('Secret', 'Secret'),
    ('Confidential', 'Confidential'),
)

graduation_year_choices = (
    ('2007', '2007'),
    ('2008', '2008'),
    ('2009', '2009'),
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'),
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
    ('2018', '2018'),

)
graduation_month_choices = (
    ('01', 'January'),
    ('02', 'February'),
    ('03', 'March'),
    ('04', 'April'),
    ('05', 'May'),
    ('06', 'June'),
    ('07', 'July'),
    ('08', 'August'),
    ('09', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)

class Person (models.Model):
    name = models.CharField(max_length=200)
    school = models.CharField(max_length=200, choices=school_choices)
    school_level = models.CharField(max_length=30, choices=school_level_choices)
    major = models.CharField(max_length=100, choices=major_choices)
    gpa = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    graduation_year = models.IntegerField(default=1900, choices=graduation_year_choices)
    graduation_month = models.IntegerField(default=0, choices=graduation_month_choices)
    language = models.CharField(max_length=200)
    skills = models.CharField(max_length=500)
    certificate = models.CharField(max_length=500)
    awards = models.CharField(max_length=500)
    conference = models.CharField(max_length=500)
    prior_company = models.CharField(max_length=100)
    year_of_experience = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    title = models.CharField(max_length=200)
    work_authorization = models.CharField(max_length=100, choices=work_authorization_choices)
    security_clearance = models.CharField(max_length=100, choices=security_clearance_choices)

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
