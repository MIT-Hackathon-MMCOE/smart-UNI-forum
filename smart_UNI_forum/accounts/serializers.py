from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                            TaggitSerializer)
from .models import Profile

class UserSerializer(UserDetailsSerializer):

    first_name  = serializers.CharField(source="Profile.user.first_name")
    last_name   = serializers.CharField(source="Profile.user.last_name")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('first_name','last_name')

    def update(self, instance, validated_data):
        profile_data    = validated_data.pop('Profile.user', {})
        first_name      = profile_data.get('first_name')
        last_name       = profile_data.get('last_name')

        instance        = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.Profile.user
        if profile_data and company_name:
            profile.company_name = company_name
            profile.save()
        return instance



class ProfileSerializer(TaggitSerializer, serializers.ModelSerializer):

    interests = TagListSerializerField()

    class Meta:
        model   = Profile
        fields  = ['first_name', 'last_name', 'interests', 'level', 'points', 'bio', 'college', 'branch', 'slug']

