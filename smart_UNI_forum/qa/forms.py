from django import forms
from django.forms import ModelForm
from .models import *

class QuestionCommentCreateForm(ModelForm):
    class Meta:
        model = QuestionComment
        fields = ['question', 'text']

    def is_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(QuestionCommentCreateForm, self).is_valid(form)
