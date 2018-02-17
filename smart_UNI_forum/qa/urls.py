"""smart_UNI_forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from .views import *
from .serializers import router

urlpatterns = [
	url(r'^api-auth/', include(router.urls)),
	url(r'^$', index, name='question_list'),
	url(r'^question/create/', QuestionCreateView.as_view(success_url="/accounts/profile/"), name='question_create'),
	url(r'^question/detail/(?P<slug>[^\.]+)/$', question_detail, name='question_detail'),
	url(r'^question/update/(?P<slug>[^\.]+)/$', QuestionUpdateView.as_view(success_url="/accounts/profile/"), name='question_update'),
	url(r'^answer/create/', AnswerCreateView.as_view(success_url="/accounts/profile/"), name='answer_create'),
	url(r'^answer/update/(?P<slug>[^\.]+)/$', AnswerUpdateView.as_view(success_url="/accounts/profile/"), name='answer_update'),
	url(r'^search/question', question_search, name='question_search')
]
