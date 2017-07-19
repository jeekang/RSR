from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from datetime import date, datetime
from django.dispatch import receiver
import string
import os
import html
# Returns a list of strings that contains related informtion about person
def Detail(person):
    # related_obj_list will be the list I will iterate through to print out each detail
    related_obj_list=[]
    # List of related sets
    model_Names=['PersonToSchool', 'PersonToCourse', 'PersonToProfessionalDevelopment', 'PersonToSide',
                  'PersonToSkills', 'PersonToLanguage' , 'PersonToClearance', 'PersonToCompany', 'PersonToAwards',
                  'PersonToClubs_Hobbies', 'PersonToVolunteering']
    for model in model_Names:
        sectionBreak='<section><b>'+model.replace('PersonTo','').replace('_',' ')+' details</b><br>'
        related_obj_list.append(sectionBreak)
        # Adjusting the model_Names to appriorate syntax for related_name reference
        # Related_names are a way to reverse foreign key
        related_name=model.lower().replace('_','')+'_set'
        related_obj=eval('person.'+related_name)
        related_obj=related_obj.all()
        # .all() for a related_obj creates a query set
        if related_obj:
            # I want to first check if related_obj has any objects if not I want to print empty. If it's not empty
            # I loop through the related_obj
            for item in related_obj:
                # Each item is a related_obj meaning persontoschool, persontocourse, etc. It's one of the intermediate
                # table objects.
                related_fields=item._meta.fields
                # I want to iterate through all fields of the intermediate table
                for field in related_fields:
                    field_name=field.get_attname()
                    # I don't want the id nor foreign key of PersonID
                    if field_name =='id' or field_name =='PersonID_id':
                        continue
                    # So if there's a _id for one of the fields it means its a foreign key. So I want to go to the foreign
                    # key.
                    if field_name.find('_id') != -1:
                        field_name=field_name.replace('_id','')
                        # modelObj is the actual object of the foreign key like school or course etc.
                        modelObj=getattr(item, field_name)
                        # I want to iterate through all fields of foreign key
                        for x in modelObj._meta.fields:
                            if x.verbose_name=='ID':
                                continue
                            x_name=x.get_attname()
                            x_value=getattr(modelObj,x_name)
                            related_obj_list.append(x.verbose_name+': '+str(x_value)+'<br>')
                    # If it's not a foreign key then I don't need to iterate through anything and I can just give you
                    # the value of the field
                    else:
                        value=getattr(item,field_name)
                        ver_name=field.verbose_name
                        related_obj_list.append(ver_name+': '+str(value)+'<br>')
        else:
            related_obj_list.append('There is no '+model+' object')
        related_obj_list.append('</section><br>')
    return related_obj_list