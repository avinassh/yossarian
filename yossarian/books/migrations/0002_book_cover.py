# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(default='covers/placeholder.jpg', upload_to='covers'),
            preserve_default=False,
        ),
    ]
