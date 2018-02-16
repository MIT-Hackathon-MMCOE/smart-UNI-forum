from rest_framework import routers, serializers, viewsets
from .serializers import ProfileSerializer
from .models import Profile

# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def parent_list(request):
        """
        List all parents.
        """
        if request.method == 'GET':
            profile = Profile.objects.get(user = request.user)
            serializer = ProfileSerializer(profile, many=False)
            return JsonResponse(serializer.data, safe=False)
        

router = routers.DefaultRouter()
router.register('profile', ProfileViewSet)