# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 19:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emapapp', '0011_auto_20171226_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='ahref',
            field=models.CharField(default=1, max_length=10000000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messages',
            name='profilename',
            field=models.CharField(default=1, max_length=1000000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='celebr',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 26, 22, 26, 56, 637041)),
        ),
    ]
