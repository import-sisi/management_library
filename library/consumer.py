from kafka import KafkaConsumer
import json
from library.models_mongo import BookSearch
from library.models import Book, Author

class Consumer:
    def __init__(self, servers, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=servers,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

    def receive_messages(self):
        for message in self.consumer:
            yield message.value

    def process_messages(self):
        for message in self.receive_messages():
            operation = message.get('operation')
            data = message.get('data')

            if operation == 'create' or operation == 'update':
                book_id = data.get('id')
                book = Book.objects.get(id=book_id)
                authors = Author.objects.filter(id__in=book.authors.values_list('id', flat=True))

                book_search = BookSearch(
                    title=book.title,
                    description=book.description,
                    publication_date=book.publication_date,
                    isbn=book.isbn,
                    price=book.price,
                    genre=book.genre.name,
                    authors=[author.id for author in authors]
                )
                book_search.save()

            elif operation == 'delete':
                book_id = data.get('id')
                BookSearch.objects(id=book_id).delete()
