# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-12-11 04:56
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20161209_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='name',
            field=models.CharField(max_length=4096, null=True),
        ),
        migrations.AlterField(
            model_name='manga',
            name='related_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=4096, null=True), default=list, size=None),
        ),
    ]