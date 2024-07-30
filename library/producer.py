from kafka import KafkaProducer
import json

class Producer:
    def __init__(self, servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def send_message(self, message):
        self.producer.send(self.topic, message)
        self.producer.flush()