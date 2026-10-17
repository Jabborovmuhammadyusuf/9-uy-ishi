from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Genre, Book
from .serializers import BookSerializer

class BookTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="Toxir")

        self.genre1 = Genre.objects.create(name="Fantastika")
        self.genre2 = Genre.objects.create(name="Detektiv")

        self.book = Book.objects.create(title="Zamon", description="Qiziqarli", price=50000, genre=self.genre1)
        self.book1 = Book.objects.create(title="Qalb", description="Sarguzasht", price=80000, genre=self.genre2)
        self.book2 = Book.objects.create(title="Alximik", description="Qiziqarli", price=60000, genre=self.genre1)

    def test_get(self):
        url = reverse('book-list')
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        serializer = BookSerializer([self.book, self.book1, self.book2], many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_search(self):
        url = reverse('book-list')
        self.client.force_login(self.user1)
        response = self.client.get(url, {'search': 'Qiziqarli'})
        self.assertEqual(response.status_code, 200)
        serializer = BookSerializer([self.book, self.book2], many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        self.client.force_login(self.user1)
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, 200)
        serializer = BookSerializer([self.book2, self.book1, self.book], many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_filter(self):
        url = reverse('book-list')
        self.client.force_login(self.user1)
        response = self.client.get(url, {'genre': self.genre1.id})
        self.assertEqual(response.status_code, 200)
        serializer = BookSerializer([self.book, self.book2], many=True)
        self.assertEqual(response.data, serializer.data)
