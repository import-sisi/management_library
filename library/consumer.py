import pika
import json
from mongoengine import connect
from .models_mongo import BookSearch

class RabbitMQConsumer:
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='book_queue')
        connect('your_mongodb_name', host='mongodb://localhost:27017')

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        # Process the message and save to MongoDB
        BookSearch(**message).save()
        print(f"Received and saved message: {message}")

    def start_consuming(self):
        self.channel.basic_consume(queue='book_queue', on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()

# Example usage
if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    consumer.start_consuming()
