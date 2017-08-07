from django import template

register=template.Library()

from RSR.models import *

@register.filter
# A preview of the details in details page
def preview_details(person):
    # A preview of the details in details page
    fields_dict = {'School':[], 'Major':[], 'GPA':[], 'Degree Level':[], 'Skills':[]}
    related_names=['persontoschool_set', 'persontoskills_set']
    for related_obj in person.persontoschool_set.all():
        fields_dict['School'].append(related_obj.SchoolID)
        fields_dict['Major'].append(related_obj.MajorID)
        fields_dict['GPA'].append(related_obj.GPA)
        fields_dict['Degree Level'].append(related_obj.SchoolID.DegreeLevel)
    for related_obj in person.persontoskills_set.all():
        fields_dict['Skills'].append(related_obj.SkillsID)
    return fields_dict

@register.filter
#Get value of a key in dictionary placed in string format
def get_key(dictionary, key):
    result=""
    for value in dictionary.get(key):
        if result == "":
            result+=str(value)
        else:
            result+=", "+str(value)
    if result == "":
        result= "N/A"
    return result
