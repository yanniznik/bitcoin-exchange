# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-24 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0016_auto_20170823_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
