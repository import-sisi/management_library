from rest_framework import generics, status
from rest_framework.response import Response
from .models import Book
from .models_mongo import BookSearch
from .serializers import BookSerializer, BookSearchSerializer
from .usecases import BookUseCase
from .repositories import BookSearchRepository
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from rest_framework.views import APIView

class BookListView(APIView):
    def get(self, request):
        filters = {
            'query': request.GET.get('query', ''),
            'min_price': request.GET.get('min_price'),
            'max_price': request.GET.get('max_price'),
            'genre': request.GET.get('genre'),
            'author_city': request.GET.get('author_city')
        }
        sort_by = request.GET.get('sort_by')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        try:
            books, total_books = BookSearchRepository.search_books(
                filters['query'],
                price_range=(filters['min_price'], filters['max_price']),
                genre=filters['genre'],
                author_city=filters['author_city'],
                sort_by=sort_by,
                page=page,
                page_size=page_size
            )
            serialized_books = BookSearchSerializer(books, many=True)
            return Response({
                'total_books': total_books,
                'books': serialized_books.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        data = self.request.data
        try:
            book = BookUseCase.create_book(data)
            return book
        except ValidationError as e:
            raise ValidationError(e)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise ObjectDoesNotExist("Book with this ID does not exist")
