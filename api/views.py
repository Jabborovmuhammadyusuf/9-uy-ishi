from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Genre, Book, Comment
from .serializers import (
    GenreSerializer,
    GenreDetailSerializer,
    BookSerializer,
    BookDetailSerializer,
    CommentSerializer,
)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all().prefetch_related('books').only('id', 'name')
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id', 'name')
    ordering = "-id"

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GenreDetailSerializer
        return GenreSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().select_related('genre').defer('description')
    serializer_class = BookSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('title', 'description')
    ordering_fields = ('id', 'title', 'price')
    filterset_fields = {
        'genre': ['exact'],
        'price': ['exact', 'lte', 'gte', 'lt', 'gt'],
    }

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().select_related('user', 'book')
    serializer_class = CommentSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('id', 'created_at')
    ordering = "-id"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
