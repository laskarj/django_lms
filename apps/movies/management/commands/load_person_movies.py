from django.core.management.base import BaseCommand
from ...models import PersonMovie, Movie, Person
import json
import re


class Command(BaseCommand):
    help = 'Load PersonMovie'

    def add_arguments(self, parser):
        parser.add_argument('-F', '--file', type=str, help='')

    def handle(self, *args, **options):
        path_file: str = f'{options["file"]}'
        with open(path_file, 'r') as file:
            while True:
                line: str = file.readline().rstrip('\n')
                if line == "":
                    break

                data: list = re.split(r'\t', line)

                person = Person.objects.filter(imdb_id=data[2]).first()
                if not person:
                    continue

                movie = Movie.objects.filter(imdb_id=data[0]).first()
                if not movie:
                    continue

                person_movies_data = {
                    'order': int(data[1]),
                    'category': data[3],
                    'job': data[4] if data[4] != '\\N' else '',
                    'characters': json.loads(data[5]) if not data[5].startswith('\\N') else None,
                }

                PersonMovie.objects.get_or_create(movie=movie, person=person, defaults=person_movies_data)
