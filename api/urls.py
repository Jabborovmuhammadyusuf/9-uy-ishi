from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, BookViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
