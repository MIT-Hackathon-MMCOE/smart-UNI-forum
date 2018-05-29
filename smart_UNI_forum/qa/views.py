# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import *
from accounts.models import *
from .choices import Labels
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


class QuestionCreateView(CreateView):
	model = Question
	fields = ['question', 'description', 'tags', 'labels']

	template_name = 'question_form.html'

	def form_valid(self, form):
		user = self.request.user
		form.instance.user = user
		return super(QuestionCreateView, self).form_valid(form)

class QuestionUpdateView(UpdateView):
	model = Question
	fields = ['question', 'description', 'tags', 'labels', 'closed']

	template_name = 'question_update_form.html'

	def form_valid(self, form):
		user 					= self.request.user
		modified 				= datetime.now()
		form.instance.user 		= user
		form.instance.modified 	= modified
		return super(QuestionUpdateView, self).form_valid(form)

class AnswerCreateView(CreateView):
	model = Answer
	fields = ['question', 'answer_text']

	template_name = 'answer_form.html'

	def form_valid(self, form):
		user = self.request.user
		form.instance.user = user
		return super(AnswerCreateView, self).form_valid(form)

class AnswerUpdateView(UpdateView):
	model = Answer
	fields = ['question', 'answer_text']

	template_name = 'answer_update_form.html'

	def form_valid(self, form):
		user 					= self.request.user
		modified 				= datetime.now()
		form.instance.user 		= user
		form.instance.modified 	= modified
		return super(AnswerUpdateView, self).form_valid(form)

class QuestionDetailView(DetailView):

	model = Question

	template_name = 'question_detail.html'

	def get_context_data(self, **kwargs):
		labels = dict(Labels)
		context = super(QuestionDetailView, self).get_context_data(**kwargs)
		return context


@login_required(login_url='/accounts/login/')
def index(request):
	user 					= Profile.objects.get(user = request.user)
	interests 				= user.interests.names()
	questions 				= Question.objects.filter(tags__name__in = interests).distinct()
	labels 					= dict(Labels)
	for question in questions:
		question.tags 		= [tag for tag in question.tags.names()]
		question.labels 	= labels[question.labels]
		question.profile 	= Profile.objects.get(user = question.user).slug

	context = {'user': user, 'questions': questions}
	return render(request, 'index-feed.html', context)


@login_required(login_url='/accounts/login/')
def question_detail(request, slug):
	if request.method == 'POST':
		form = AnswerCommentCreateForm(request.POST)
		if form.is_valid():
			instance 		= form.save(commit=False)
			instance.user 	= request.user
			instance.answer = Answer.objects.get(slug = self.slug)
			instance.save()

		form = QuestionCommentCreateForm(request.POST)
		if form.is_valid():
			instance 			= form.save(commit=False)
			instance.user 		= request.user
			instance.question 	= Question.objects.get(slug = self.slug)
			instance.save()

	question 			= Question.objects.get(slug = slug)
	user 				= Profile.objects.get(user = question.user)
	labels 				= dict(Labels)
	question.tags 		= [tag for tag in question.tags.names()]
	question.labels 	= labels[question.labels]
	question.comments 	= QuestionComment.objects.filter(question = question)
	answers				= Answer.objects.filter(question = question)
	for answer in answers:
		answer.profile  = Profile.objects.get(user = answer.user).slug
		answer.comments = [comment for comment in AsnwerComment.objects.filter(answer = answer)]
	ans_c_form 			= AnswerCommentCreateForm()
	ans_form 			= AnswerCreateForm()
	ques_c_form			= QuestionCommentCreateForm()
	context 			= {'user': user, 'question': question, 'answers': answers, 'ques_c_form': ques_c_form, 'ans_form': ans_form, 'ans_c_form': ans_c_form}
	return render(request, 'question_detail.html', context)

@method_decorator(csrf_exempt, name='question_search')
def question_search(request):
	if request.method == 'POST':
		key = request.POST.get("data.key", "")
		questions 	= Question.objects.filter(question__contains=key)
		temp 		= ''
		for question in questions:
			temp += "<h4><a href='/question/detail/" + str(question.slug) + "/'>" + question.question +"</a></h4>"
		return HttpResponse(temp)


def follow_user(request):
	return HttpResponse("Okay")