# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-12-08 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_manga_related_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emailed_at',
            field=models.DateTimeField(null=True),
        ),
    ]
