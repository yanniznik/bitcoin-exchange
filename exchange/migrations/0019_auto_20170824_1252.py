# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-24 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0018_auto_20170824_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.png', null=True, upload_to=''),
        ),
    ]
