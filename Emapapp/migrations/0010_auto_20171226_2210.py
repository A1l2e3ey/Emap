# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 19:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emapapp', '0009_auto_20171226_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celebr',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 26, 22, 10, 25, 851331)),
        ),
    ]