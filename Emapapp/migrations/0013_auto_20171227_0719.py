# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-27 04:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emapapp', '0012_auto_20171226_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='your',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 27, 7, 19, 5, 318741)),
        ),
        migrations.AlterField(
            model_name='celebr',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 27, 7, 19, 5, 317739)),
        ),
    ]
