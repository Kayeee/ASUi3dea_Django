# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ASUi3dea', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inverter',
            name='latitude',
            field=models.FloatField(default=33.3059398),
        ),
        migrations.AddField(
            model_name='inverter',
            name='longitude',
            field=models.FloatField(default=-111.6792469),
        ),
    ]
