from rest_framework import serializers
from django.contrib.auth import get_user_model
from main.models import Post, Brand, CarModel

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['make']

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    make = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','make', 'model', 'author', 'price']

    
    def get_make(self, obj):
        return BrandSerializer(obj.make).data
    
    def get_model(self, obj):
        return ModelSerializer(obj.model).data
    
    def get_author(self, obj):
        return UserSerializer(obj.author).data