from rest_framework import serializers
from rest_framework import routers, serializers, viewsets
from taggit_serializer.serializers import (TagListSerializerField,
											TaggitSerializer)
from .models import Question
from .choices import Labels

class QuestionSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):

	tags = TagListSerializerField()

	class Meta:
		model   = Question
		fields  = ['url', 'slug', 'question', 'tags', 'labels', 'closed', 'created', 'attachment']

class  QuestionViewSet(viewsets.ModelViewSet):
	queryset 	= Question.objects.all()
	serializer_class = QuestionSerializer
	
	def question_list():
		if request.method == 'GET':
			user 			= Profile.objects.get(user = request.user)
			interests 		= user.interests.names()
			question 		= Question.objects.filter(tags__name__in = interests).distinct()
			labels 			= dict(Labels)
			for ques in question:
				ques.tags 		= [tag for tag in ques.tags.names()]
				ques.labels 	= labels[ques.labels]
			serializer 		= QuestionSerializer(question, many=False)
			return JsonResponse(serializer.data, safe=False)
		
router = routers.SimpleRouter()
router.register('question', QuestionViewSet, 'question')