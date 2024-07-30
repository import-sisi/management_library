from django.urls import path
from .views import BookListView, BookListCreateView, BookRetrieveUpdateDeleteView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/search/', BookListView.as_view(), name='book-search'),  # New endpoint for searching books
    path('books/create/', BookListCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-detail'),
]
