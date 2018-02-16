# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
# from taggit.managers import TaggableManager
from django.db import models
# from django_markdown.models import MarkdownField
from django.contrib.auth.models import User


UserModel = get_user_model()

# Create your models here.
class Activation(models.Model):
	user 			= models.ForeignKey(UserModel, on_delete=models.CASCADE)
	created_at  	= models.DateTimeField(auto_now_add=True)
	code 			= models.CharField(max_length=20)
	email 			= models.EmailField(blank=True)

class Profile(models.Model):
	user 			= models.ForeignKey(UserModel, on_delete = models.CASCADE)
	attachment		= models.ImageField(upload_to='profile-images/')
	level			= models.IntegerField()
	points 			= models.IntegerField(default=0)
	# clg
	# branch

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
	user 			= models.ForeignKey(User, related_name="User")
	following 		= models.ForeignKey(User, related_name="Following")
	class Meta:
		unique_together = ('user', 'following')


class Projects(models.Model):
	"""docstring for Projects"""
	title 		= models.CharField(max_length = 200)
	description = models.CharField(max_length = 600)
	url 		= models.URLField()
	upload 		= models.FileField(upload_to='projects/')
	user 		= models.ForeignKey(User)



# # Create your models here.

# class Question(models.Model):
# 	"""docstring for Question"""
# 	slug 			= models.SlugField(max_length=200)
# 	question 		= models.CharField(max_length = 200)
# 	description		= MarkdownField()
# 	tags  			= TaggableManager()
# 	upvotes 		= models.PositiveIntegerField(default = 0)
# 	downvotes 		= models.PositiveIntegerField(default = 0)
# 	closed  		= models.BooleanField(default=False)
# 	flagged			= models.PositiveIntegerField(default = 0)
# 	user			= models.ForeignKey(User)
# 	created			= models.DateTimeField('date published', auto_now_add=True)
# 	modified		= models.DateTimeField('date updated', auto_now=True)
# 	attachment 		= models.ImageField(upload_to='images/')

# 	def __str__(self):
# 		return self.question

# class Answer(models.Model):
# 	"""Model class to contain every answer in the forum and to link it
# 	to the proper question."""
# 	question 		 = models.ForeignKey(Question)
# 	answer_text 	 = MarkdownField()
# 	created			 = models.DateTimeField('date published', auto_now_add=True)
# 	modified		 = models.DateTimeField('date updated', auto_now=True)
# 	user 			 = models.ForeignKey(User)
# 	upvotes 		 = models.IntegerField(default=0)
# 	downvotes		 = models.IntegerField(default=0)
# 	slug 			 = models.SlugField(max_length=200)

# 	def __str__(self):
# 		return self.answer_text


# class QuestionComment(models.Model):
# 	"""docstring for QuestionComment"""
# 	user 			= models.ForeignKey(User)
# 	answer 			= models.ForeignKey(Answer)
# 	text 			= models.CharField(max_length = 200)
# 	created			= models.DateTimeField('date published', auto_now_add = True)
# 	slug 			= models.SlugField(max_length=200)

# class AnswerComment(models.Model):
# 	"""docstring for AnswerComment"""
# 	user 			= models.ForeignKey(User)
# 	answer 			= models.ForeignKey(Answer)
# 	text 			= models.CharField(max_length = 200)
# 	created			= models.DateTimeField('date published', auto_now_add = True)
# 	slug 			= models.SlugField(max_length=200)


# class QuestionUpvote(models.Model):
# 	"""docstring for question upvotes"""
# 	post 	 = models.ForeignKey(Question)
# 	liked_by = models.ForeignKey(User)

# class AnswerUpvote(models.Model):
# 	"""docstring for answer upvotes"""
# 	post 	 = models.ForeignKey(Answer)
# 	liked_by = models.ForeignKey(User)
