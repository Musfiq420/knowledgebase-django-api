from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Notebook, Category, Article, Comment


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = ['id', 'name', 'created_by', 'shared_with', 'created_at', 'updated_at']
        extra_kwargs = {'created_by': {'read_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'notebook', 'user']
        extra_kwargs = {'user': {'read_only': True}}

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'category', 'notebook', 'user', 'created_at', 'updated_at']
        extra_kwargs = {'user': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'text', 'created_at', 'updated_at']
        extra_kwargs = {'user': {'read_only': True}}