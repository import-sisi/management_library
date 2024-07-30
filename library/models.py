from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .producer import Producer

# Initialize the producer
producer = Producer(servers=['localhost:9092'], topic='book_topic')

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        book_data = {
            'title': self.title,
            'description': self.description,
            'publication_date': str(self.publication_date),
            'isbn': self.isbn,
            'price': float(self.price),
            'genre': self.genre.name,
            'authors': [author.id for author in self.authors.all()]
        }
        producer.send_message({'operation': 'create', 'data': book_data})

@receiver(post_save, sender=Book)
def post_save_book(sender, instance, **kwargs):
    instance.save()