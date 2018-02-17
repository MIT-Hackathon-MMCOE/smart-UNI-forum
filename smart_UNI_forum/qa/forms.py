from django import forms
from django.forms import ModelForm
from .models import *

class QuestionCommentCreateForm(ModelForm):
    question = forms.CharField(required=True, max_length=50, widget=forms.HiddenInput())
    class Meta:
        model = QuestionComment
        fields = ['question','text']

class AnswerCommentCreateForm(ModelForm):
    answer = forms.CharField(required=True, max_length=50, widget=forms.HiddenInput())
    class Meta:
        model = AnswerComment
        fields = ['answer','text']

class SearchForm(forms.Form):
	key = forms.CharField(required = True, max_length=200, widget =forms.TextInput())
	fields = ['key']