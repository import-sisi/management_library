import pika
import json


class RabbitMQProducer:
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='book_queue')

    def send_message(self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key='book_queue',
            body=json.dumps(message)
        )

    def close(self):
        self.connection.close()

# Example usage
# producer = RabbitMQProducer()
# producer.send_message({'key': 'value'})
# producer.close()
