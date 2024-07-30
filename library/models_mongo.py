from mongoengine import Document, StringField, FloatField, IntField, ListField, DateField

class BookSearch(Document):
    title = StringField(max_length=200)
    description = StringField()
    publication_date = DateField()
    isbn = StringField(max_length=13)
    price = FloatField()
    genre = StringField(max_length=100)
    authors = ListField(IntField())

    meta = {'collection': 'books'}