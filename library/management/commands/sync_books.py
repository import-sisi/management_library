from django.core.management.base import BaseCommand
from library.consumer import Consumer

class Command(BaseCommand):
    help = 'Sync books from SQL database to MongoDB using Kafka'

    def handle(self, *args, **kwargs):
        consumer = Consumer(servers=['localhost:9092'], topic='book_transfers')
        consumer.process_messages()