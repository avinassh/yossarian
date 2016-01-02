# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 16:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import yossarian.books.validators


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_is_contestant'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('week_number', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(53), django.core.validators.MinValueValidator(1)])),
                ('week_date', models.DateField(validators=[yossarian.books.validators.is_monday])),
                ('is_english', models.BooleanField()),
                ('on_homepage', models.BooleanField(default=False)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
            ],
            options={
                'ordering': ['week_number'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='weeklybook',
            unique_together=set([('week_number', 'is_english')]),
        ),
    ]