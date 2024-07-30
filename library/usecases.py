# usecases.py
from .repositories import BookRepository
from .serializers import BookSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class BookUseCase:
    @staticmethod
    def list_books():
        books = BookRepository.get_all_books()
        return BookSerializer(books, many=True).data

    @staticmethod
    def retrieve_book(book_id):
        try:
            book = BookRepository.get_book_by_id(book_id)
            return BookSerializer(book).data
        except ObjectDoesNotExist as e:
            raise e

    @staticmethod
    def create_book(data):
        try:
            book = BookRepository.create_book(data)
            return BookSerializer(book).data
        except ValidationError as e:
            raise e

    @staticmethod
    def update_book(book_id, data):
        try:
            book = BookRepository.update_book(book_id, data)
            return BookSerializer(book).data
        except ObjectDoesNotExist as e:
            raise e

    @staticmethod
    def delete_book(book_id):
        try:
            message = BookRepository.delete_book(book_id)
            return message
        except ObjectDoesNotExist as e:
            raise e

    @staticmethod
    def search_books(filters, sort_by):
        try:
            books = BookRepository.search_books(filters, sort_by)
            return books
        except Exception as e:
            raise e
