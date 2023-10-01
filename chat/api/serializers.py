from rest_framework import serializers
from django.contrib.auth import get_user_model
from chat.models import Message, Conversation
from main.api.serializers import PostSerializer
from main.models import Post

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'from_user',
            'to_user',
            'content',
            'timestamp',
        ]

    def get_from_user(self, obj):
        return UserSerializer(obj.from_user).data
    
    def get_to_user(self, obj):
        return UserSerializer(obj.to_user).data


class ConversationSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = (
            'id',
            'name',
            'post',
        )

    def get_post(self, obj):
        return PostSerializer(obj.post).data