# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='industry',
            name='id',
        ),
        migrations.AddField(
            model_name='industry',
            name='industry_id',
            field=models.BigIntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
