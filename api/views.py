from django.contrib.auth import authenticate
from rest_framework import viewsets,generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import Notebook, Category, Article, Comment
from .serializers import NotebookSerializer, CategorySerializer, ArticleSerializer, CommentSerializer, UserRegisterSerializer, UserLoginSerializer

class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "message": "Login successful!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)

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