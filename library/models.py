from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .producer import RabbitMQProducer

# Initialize the producer

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_city = models.ForeignKey(City, on_delete=models.CASCADE)

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    authors = models.ManyToManyField(Author)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)



@receiver(post_save, sender=Book)
def send_book_to_mongodb(sender, instance, **kwargs):
    authors = [author.id for author in instance.authors.all()]
    book_data = {
        'title': instance.title,
        'description': instance.description,
        'publication_date': str(instance.publication_date),
        'isbn': instance.isbn,
        'price': float(instance.price),
        'authors': authors,
        'genre': instance.genre.name,
    }
    producer = RabbitMQProducer()
    producer.send_message(book_data)
    producer.close()