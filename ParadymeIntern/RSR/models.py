# -*- coding: utf-8 -*-
import os

from django.db import models
from django.dispatch import receiver



class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y%m%d')



#@receiver(models.signals.post_delete, sender=Document)
#def auto_delete_file_on_delete(sender, instance, **kwargs):

    #if instance.file:
        #if os.path.isfile(instance.file.path):
         #   os.remove(instance.file.path)
