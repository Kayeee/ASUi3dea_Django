# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-14 00:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASUi3dea', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mode',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 14, 0, 38, 22, 976367)),
        ),
        migrations.AddField(
            model_name='temperature',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 14, 0, 38, 22, 975794)),
        ),
    ]
