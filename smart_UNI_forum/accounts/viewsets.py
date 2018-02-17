from rest_framework import routers, serializers, viewsets
from .serializers import ProfileSerializer
# , UserSerializer
from django.contrib.auth.models import User
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

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def user_list(request):
#         """
#         List all parents.
#         """
#         if request.method == 'GET':
#             user        = User.objects.get(user = request.user)
#             serializer  = UserSerializer(user, many=False)
#             return JsonResponse(serializer.data, safe=False)
        

#     def user_details(self, request, pk=None):
#         """
#         Returns a list of all the group names that the given
#         user belongs to.
#         """
#         user        = UserModel.objects.get(id = request.pk)
#         serializer  = UserSerializer(user, many = False)
#         return JsonResponse(serializer.data, safe=False)

router = routers.SimpleRouter()
router.register('profile', ProfileViewSet, 'profile')
# router.register('user', UserViewSet, 'user')