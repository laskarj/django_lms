import os.path

from django.core.management.base import BaseCommand
from ...models import Person
import csv


class Command(BaseCommand):
    help = 'Import Persons from tsv file'

    def add_arguments(self, parser):
        parser.add_argument('-F', '--file', type=str, help='')

    def handle(self, *args, **options):
        file_name = options.get('file')

        if not os.path.exists(file_name):
            print('No file exist.')

        with open(file_name, 'r') as f:
            reader = csv.DictReader(f, dialect=csv.excel_tab, fieldnames=['imdb_id',
                                                                          'name',
                                                                          'birth_date',
                                                                          'death_date',
                                                                          'primary_profession',
                                                                          'know_for'])
            # reader.__next__()  # if csv file first line is header

            for line in reader:
                person_date = line
                imdb_id = person_date['imdb_id']
                person_date.pop('primary_profession')
                person_date.pop('know_for')

                if person_date['birth_date'] == '\\N':
                    person_date['birth_date'] = None
                else:
                    person_date['birth_date'] = f'{person_date["birth_date"]}-01-01'

                if person_date['death_date'] == '\\N':
                    person_date['death_date'] = None
                else:
                    person_date['death_date'] = f'{person_date["death_date"]}-01-01'

                person, created = Person.objects.get_or_create(imdb_id=imdb_id, defaults=person_date)



            if not created:
                Person.objects.filter(id=person.id).update(**person_date)

