# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 10:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_attachment_upload_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='upload_date',
        ),
    ]
