# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-12-11 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20161211_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='notification_frequency',
            field=models.CharField(choices=[('never', 'never'), ('noonly', 'noonly'), ('daily', 'daily'), ('bidaily', 'bidaily'), ('weekly', 'weekly'), ('biweekly', 'biweekly'), ('monthly', 'monthly'), ('bimonthly', 'bimonthly')], default='never', max_length=32),
        ),
    ]
