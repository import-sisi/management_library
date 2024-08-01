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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine import Q
from library.models_mongo import BookSearch
from library.serializers import BookSearchSerializer

class BookSearchView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', '')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        genre = request.query_params.get('genre')
        author_id = request.query_params.get('author_id')
        sort_by = request.query_params.get('sort_by', 'price')

        filters = Q()
        if search_query:
            filters &= Q(title__icontains=search_query) | Q(description__icontains=search_query)
        if min_price:
            filters &= Q(price__gte=float(min_price))
        if max_price:
            filters &= Q(price__lte=float(max_price))
        if genre:
            filters &= Q(genre=genre)
        if author_id:
            filters &= Q(authors=author_id)

        books = BookSearch.objects(filters).order_by(sort_by)

        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        total_books = books.count()

        books = books[start:end]

        serializer = BookSearchSerializer(books, many=True)
        return Response({
            'total': total_books,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    
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
