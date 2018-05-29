# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from taggit.managers import TaggableManager
from django.db import models
# from django_markdown.models import MarkdownField
from .choices import *
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your models here.
class Activation(models.Model):
	user 			= models.OneToOneField(UserModel, on_delete=models.CASCADE)
	created_at  	= models.DateTimeField(auto_now_add=True)
	code 			= models.CharField(max_length=20)
	email 			= models.EmailField(blank=True)

class Profile(models.Model):
	user 			= models.OneToOneField(UserModel, on_delete = models.CASCADE)
	first_name		= models.CharField(max_length = 50)
	last_name		= models.CharField(max_length = 50)
	profile_pic 	= models.ImageField(upload_to='profile-images/', blank = True)
	level			= models.IntegerField(default = 1)
	interests		= TaggableManager()
	bio				= models.CharField(max_length = 250)
	points 			= models.IntegerField(default=0)
	college 	 	= models.CharField(max_length=20, choices = Colleges)
	branch			= models.CharField(max_length=20, choices = Branch)
	slug 			= models.SlugField(max_length = 60, unique = True)

	def save(self):
		if not self.pk:
			self.slug = slugify(self.get_full_name() + " " + self.user.email)
		super(Profile, self).save()

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		if self.first_name and self.last_name:
			full_name = '%s %s' % (self.first_name, self.last_name)
		else:
			full_name = '%s %s' % (self.user.first_name, self.user.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.user.first_name

class Follower(models.Model):
	"""docstring for Followers"""
	user 			= models.ForeignKey(UserModel, related_name="User")
	following 		= models.ForeignKey(UserModel, related_name="Following")
	class Meta:
		unique_together = ('user', 'following')

class Project(models.Model):
	"""docstring for Projects"""
	title 		= models.CharField(max_length = 200)
	description = models.CharField(max_length = 600)
	url 		= models.URLField()
	# upload 		= models.FileField(upload_to='projects/', blank=True)
	user 		= models.ForeignKey(UserModel)