from rest_framework import serializers
from .models import Genre, Book, Comment

class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'price']

class GenreSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'

class GenreDetailSerializer(serializers.ModelSerializer):
    books = BookInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())

    class Meta:
        model = Book
        fields = '__all__'

class BookDetailSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_genre(self, obj):
        return {
            'id': obj.genre.id,
            'name': obj.genre.name
        }

    def get_course(self, obj):
        return {
            'id': obj.genre.id,
            'name': obj.genre.name
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created_at']
