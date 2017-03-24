# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 13:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0001_initial'),
        ('feedsource', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedsource',
            name='periodic_task',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.PeriodicTask'),
        ),
    ]