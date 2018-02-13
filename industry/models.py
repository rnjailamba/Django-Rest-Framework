# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Industry(models.Model):
    name = models.CharField(max_length=255)
    industry_id = models.CharField(max_length=255, primary_key=True)
    direct_parent_id = models.CharField(max_length=255, null=True)
    parent_ids = ArrayField(models.CharField(max_length=255), null=True)