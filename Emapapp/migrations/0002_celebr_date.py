# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 17:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emapapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='celebr',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
