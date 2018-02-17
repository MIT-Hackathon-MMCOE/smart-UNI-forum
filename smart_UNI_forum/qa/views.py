# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import *

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
        context = super().get_context_data(**kwargs)
        context['labels'] 	= labels[question.labels]
        context['tags'] 	= [tag for tag in question.tags.names()]
        return context