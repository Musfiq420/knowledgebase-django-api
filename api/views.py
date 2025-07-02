import os
from django.contrib.auth import authenticate
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets,generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import Notebook, Category, Article, Comment
from .serializers import NotebookSerializer, CategorySerializer, ArticleSerializer, CommentSerializer, UserSerializer

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv("GOOGLE_REDIRECT_URL")
    client_class = OAuth2Client

class UserMe(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class NotebookViewSet(viewsets.ModelViewSet):
    serializer_class = NotebookSerializer

    def get_queryset(self):
        # Show books created by or shared with the user
        return Notebook.objects.filter(created_by=self.request.user) | Notebook.objects.filter(shared_with=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(notebook__created_by=self.request.user) | Category.objects.filter(notebook__shared_with=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(notebook__created_by=self.request.user) | Article.objects.filter(notebook__shared_with=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(article__notebook__created_by=self.request.user) | Comment.objects.filter(article__notebook__shared_with=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)