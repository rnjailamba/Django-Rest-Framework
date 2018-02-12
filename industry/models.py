# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models


class Industry(models.Model):
    name = models.CharField(max_length=255)
    industry_id = models.BigIntegerField(primary_key=True)
