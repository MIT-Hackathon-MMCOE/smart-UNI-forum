from rest_framework import routers, serializers, viewsets
from .serializers import ProfileSerializer
from .models import Profile

# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def profile_list(request):
        """
        List all parents.
        """
        if request.method == 'GET':
            profile = Profile.objects.get(user = request.user)
            serializer = ProfileSerializer(profile, many=False)
            return JsonResponse(serializer.data, safe=False)
        

    def profile_details(self, request, pk=None):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        user        = UserModel.objects.get(id = request.pk)
        profile     = Profile.objects.get(user = user)
        serializer  = ProfileSerializer(profile, many = False)
        return JsonResponse(serializer.data, safe=False)

router = routers.SimpleRouter()
router.register('profile', ProfileViewSet, 'profile')