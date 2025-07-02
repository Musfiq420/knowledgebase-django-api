from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotebookViewSet, CategoryViewSet, ArticleViewSet, CommentViewSet
from .views import GoogleLogin,UserMe

router = DefaultRouter()
router.register(r'notebooks', NotebookViewSet, basename='notebook')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('users/me/', UserMe.as_view(), name='user_detail'),
    path('', include(router.urls)),
]