from rest_framework import serializers
from .models import City, Author, Genre, Book
from .models_mongo import BookSearch

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# class BookSearchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookSearch
#         fields = '__all__'
from rest_framework import serializers
from library.models_mongo import BookSearch

class BookSearchSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    publication_date = serializers.DateField()
    isbn = serializers.CharField(max_length=13)
    price = serializers.FloatField()
    genre = serializers.CharField(max_length=100)
    authors = serializers.ListField(child=serializers.IntegerField())