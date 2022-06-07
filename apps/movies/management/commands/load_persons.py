from django.core.management.base import BaseCommand
from ...models import Person
import re


class Command(BaseCommand):
    help = 'Load Persons'

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
                if data[2] == "\\N":
                    data[2] = None
                else:
                    data[2] += '-12-31'

                if data[3] == "\\N":
                    data[3] = None
                else:
                    data[3] += '-12-31'

                persons = Person(data[0], data[1], data[2], data[3])
                persons.save()
