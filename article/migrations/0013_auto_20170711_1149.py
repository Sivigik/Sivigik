# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-11 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20170711_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='file',
            field=models.FileField(null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
