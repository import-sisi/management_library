from mongoengine import connect
from .models_mongo import BookSearch
from .models import Book, Author, Genre

from .producer import RabbitMQProducer
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# Connect to MongoDB
connect(
    db='booklib_db',
    host='localhost',
    port=27017,
    username='',
    password=''
)



producer = RabbitMQProducer(servers=['localhost:9092'], topic='book_transfers')

class BookRepository:
    @staticmethod
    def create_book(data):
        if Book.objects.filter(isbn=data.get('isbn')).exists():
            raise ValidationError("A book with this ISBN already exists")

        authors_data = data.pop('authors', [])
        genre_id = data.pop('genre')
        genre = Genre.objects.get(id=genre_id)
        book = Book.objects.create(genre=genre, **data)
        if authors_data:
            authors = Author.objects.filter(id__in=authors_data)
            book.authors.set(authors)
        
        # Send book data to Kafka
        producer.send_message({'operation': 'create', 'data': data})
        
        return book

    @staticmethod
    def update_book(book_id, data):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise ObjectDoesNotExist("Book with this ID does not exist")

        authors_data = data.pop('authors', None)
        genre_id = data.pop('genre', None)

        if genre_id is not None:
            genre = Genre.objects.get(id=genre_id)
            book.genre = genre

        if authors_data is not None:
            authors = Author.objects.filter(id__in=authors_data)
            book.authors.set(authors)

        for key, value in data.items():
            setattr(book, key, value)

        book.save()

        # Send book data to Kafka
        producer.send_message({'operation': 'update', 'data': data})

        return book

    @staticmethod
    def delete_book(book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()

            # Send book data to Kafka
            producer.send_message({'operation': 'delete', 'data': {'id': book_id}})
        except Book.DoesNotExist:
            raise ObjectDoesNotExist("Book with this ID does not exist")


class BookSearchRepository:
    @staticmethod
    def search_books(query, price_range=None, genre=None, author_city=None, sort_by=None, page=1, page_size=10):
        books = BookSearch.objects(title__icontains=query) | BookSearch.objects(description__icontains=query)
        
        if price_range:
            min_price, max_price = price_range
            books = books.filter(price__gte=min_price, price__lte=max_price)
        
        if genre:
            books = books.filter(genre=genre)
        
        if author_city:
            books = books.filter(authors__in=author_city)
        
        if sort_by:
            if sort_by == 'cheapest':
                books = books.order_by('price')
            elif sort_by == 'expensive':
                books = books.order_by('-price')
        
        total_books = books.count()
        books = books.skip((page - 1) * page_size).limit(page_size)
        
        return books, total_books
