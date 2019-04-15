# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Product(models.Model):
	sku  = models.CharField(max_length=255,  null=False,primary_key=True)
	asin  = models.CharField(max_length=255,  null=False)
	quantity  = models.DecimalField(max_digits=10, decimal_places=2)
	price  = models.DecimalField(max_digits=50, decimal_places=2)

class Price(models.Model):
	product_id = models.CharField(max_length=8,  null=False)
	quantity  = models.DecimalField(max_digits=10, decimal_places=2)
	price  = models.DecimalField(max_digits=50, decimal_places=2)
