from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from datetime import date, datetime
from django.dispatch import receiver
import string
import os

# Returns a list of strings that contains related informtion about person
def Detail(person):
    related_obj_list=[]

    # I'm listing all information related to school separate from restof code since its a special case where I need
    # to access more than one field of a PersonToModel table
    schoolNames=['School: ', 'Degree Level: ', 'Major: ', 'Graduation Date: ', 'GPA: ']
    schoolInfo=['SchoolID', 'SchoolID.DegreeLevel','MajorID', 'GradDate', 'GPA']
    for item in person.persontoschool_set.all():
        currPos=0
        for info in schoolInfo:
            itemInfo=eval('item.'+info)
            try:
                related_obj_list.append(schoolNames[currPos]+str(itemInfo))
            except:
                related_obj_list.append(schoolNames[currPos]+'N/A')
            currPos+=1
        currPos=0

    # This is the related_set names, I add the personto and _set part to it later on for preference purposes only
    relatedNames = ['course', 'professionaldevelopment', 'side', 'skills', 'language'
        , 'clearence', 'company', 'awards', 'clubshobbies', 'volunteering']
    # This is the foreign key reference to the models
    modelReferences = ['CourseID', 'ProfID', 'SideID', 'SkillsID', 'LangID', 'ClearenceLevel',
                       'CompanyName', 'AwardName', 'CHName', 'VolunName']
    # Loops through every model
    position=0
    for related in relatedNames:
        # Get the related set of each model
        # The default related set is the name of intermediary table, lowercased + _set
        # The related set is used to reverse foreign keys and you access it by currentmodel.related_set where
        # the related_set is where the foreign key to current model stems from
        string = 'personto'+related+'_set'
        related_obj = eval('person.'+string)
        # Related_obj cannot be iterated unless put in a query set so I put in a query set using all()
        related_obj = related_obj.all()
        # Default value if there's no value should be N/A
        value='N/A'
        # There should only be 1 object in this query set
        for item in related_obj:
            # I want to do something grab the exact field of the item so I use getattr
            item=getattr(item,modelReferences[position])
            # Finally I add the string I want to be displayed into related_obj_list which I will iterate through in
            # details template
            value=str(item)
        related_obj_list.append(related.capitalize()+': ' +value)
        position+=1
    return related_obj_list
