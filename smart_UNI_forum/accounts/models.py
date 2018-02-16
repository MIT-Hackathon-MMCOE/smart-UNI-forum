# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from taggit.managers import TaggableManager
from django.db import models
# from django_markdown.models import MarkdownField
from .choices import *



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
 	profile_pic 	= models.ImageField(upload_to='profile-images/')
 	level			= models.IntegerField()
	points 			= models.IntegerField(default=0)
	college 	 	= models.CharField(max_length=20, choices = Colleges)
	branch			= models.CharField(max_length=20, choices = Branch)
	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		full_name = '%s %s' % (self.user.first_name, self.user.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.user.first_name

	def get_followers(self):
		list(Follower.objects.filter(following = self.pk))

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
	upload 		= models.FileField(upload_to='projects/')
	user 		= models.ForeignKey(UserModel)


