# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

# Create your models here.
class Activation(models.Model):
	user 		= models.ForeignKey(UserModel, on_delete=models.CASCADE)
	created_at  = models.DateTimeField(auto_now_add=True)
	code 		= models.CharField(max_length=20)
	email 		= models.EmailField(blank=True)

