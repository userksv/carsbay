from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Profile
User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'image']