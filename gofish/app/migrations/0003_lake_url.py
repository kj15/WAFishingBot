# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20161114_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='lake',
            name='url',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
