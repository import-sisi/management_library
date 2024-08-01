from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDeleteView
from library.views import BookSearchView

urlpatterns = [
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    # path('books/', BookListView.as_view(), name='book-list'),
    # path('books/search/', BookListView.as_view(), name='book-search'),  # New endpoint for searching books
    path('books/create/', BookListCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-detail'),
]
