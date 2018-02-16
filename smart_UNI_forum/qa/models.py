# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from taggit.managers import TaggableManager
from django_markdown.models import MarkdownField

from django.contrib.auth import get_user_model
UserModel = get_user_model()
# Create your models here.

class Question(models.Model):
	"""docstring for Question"""
	slug 			= models.SlugField(max_length=200)
	question 		= models.CharField(max_length = 200)
	description		= MarkdownField()
	tags  			= TaggableManager()
	upvotes 		= models.PositiveIntegerField(default = 0)
	downvotes 		= models.PositiveIntegerField(default = 0)
	closed  		= models.BooleanField(default=False)
	flagged			= models.PositiveIntegerField(default = 0)
	user			= models.ForeignKey(UserModel)
	created			= models.DateTimeField('date published', auto_now_add=True)
	modified		= models.DateTimeField('date updated', auto_now=True)
	attachment 		= models.ImageField(upload_to='images/')

	def save(self):
		self.slug = slugify(self.get_full_name())
		super(Profile, self).save()

	def __str__(self):
		return self.question

class Answer(models.Model):
	"""Model class to contain every answer in the forum and to link it
	to the proper question."""
	question 		 = models.ForeignKey(Question)
	answer_text 	 = MarkdownField()
	created			 = models.DateTimeField('date published', auto_now_add=True)
	modified		 = models.DateTimeField('date updated', auto_now=True)
	user 			 = models.ForeignKey(UserModel)
	upvotes 		 = models.IntegerField(default=0)
	downvotes		 = models.IntegerField(default=0)
	slug 			 = models.SlugField(max_length=200)

	def __str__(self):
		return self.answer_text


class QuestionComment(models.Model):
	"""docstring for QuestionComment"""
	user 			= models.ForeignKey(UserModel)
	answer 			= models.ForeignKey(Answer)
	text 			= models.CharField(max_length = 200)
	created			= models.DateTimeField('date published', auto_now_add = True)
	slug 			= models.SlugField(max_length=200)

class AnswerComment(models.Model):
	"""docstring for AnswerComment"""
	user 			= models.ForeignKey(UserModel)
	answer 			= models.ForeignKey(Answer)
	text 			= models.CharField(max_length = 200)
	created			= models.DateTimeField('date published', auto_now_add = True)
	slug 			= models.SlugField(max_length=200)


class QuestionUpvote(models.Model):
	"""docstring for question upvotes"""
	post 	 = models.ForeignKey(Question)
	liked_by = models.ForeignKey(UserModel)

class AnswerUpvote(models.Model):
	"""docstring for answer upvotes"""
	post 	 = models.ForeignKey(Answer)
	liked_by = models.ForeignKey(UserModel)
