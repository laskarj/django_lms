from django.core.management.base import BaseCommand
from ...models import Movie
import re


class Command(BaseCommand):
    help = 'Load Movies'

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

                if data[5] == "\\N":
                    data[5] = None

                else:
                    data[5] += '-12-31'

                data[8] = data[8].split(',')

                movie = Movie(data[0], data[1], data[2], data[4], data[5], data[8])
                movie.save()
