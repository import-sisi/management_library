import json
from django.core.management.base import BaseCommand
from library.models import City, Genre, Author

class Command(BaseCommand):
    help = 'Load initial data from a JSON file'

    def handle(self, *args, **kwargs):
        with open('initial_data.json', 'r') as file:
            data = json.load(file)

        for item in data:
            model = item['model']
            pk = item['pk']
            fields = item['fields']

            if model == 'library.city':
                City.objects.update_or_create(pk=pk, defaults=fields)
            elif model == 'library.genre':
                Genre.objects.update_or_create(pk=pk, defaults=fields)
            elif model == 'library.author':
                birth_city_id = fields.pop('birth_city')
                birth_city = City.objects.get(pk=birth_city_id)
                fields['birth_city'] = birth_city
                Author.objects.update_or_create(pk=pk, defaults=fields)

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
