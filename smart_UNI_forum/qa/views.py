# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import *

class QuestionCreateView(CreateView):
    model = Question
    fields = ['question', 'description', 'tags', 'labels']

    template_name = 'question_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(QuestionCreateView, self).form_valid(form)

# Create your views here.
