# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-24 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RSR', '0008_auto_20170721_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persontocompany',
            name='EndDate',
            field=models.DateField(default=24, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='persontocompany',
            name='StartDate',
            field=models.DateField(default=24, verbose_name='Start Date'),
        ),
    ]
