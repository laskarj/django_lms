import os.path
import json

from django.core.management.base import BaseCommand, CommandError

from apps.imdb.models import Movie, Person, PersonMovie


class Command(BaseCommand):
    help = "Imorts personmovies from tsv file"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, required=True)

    def handle(self, *args, **options):
        file_name = options.get("file")

        if not os.path.exists(file_name):
            raise CommandError("No file exists.")

        with open(file_name, encoding="utf-8") as f:
            for line in f.readlines():
                if not line:
                    continue
                if not line.startswith("tt"):
                    continue
                data = line.split("\t")

                person = Person.objects.filter(imdb_id=data[2]).first()
                if not person:
                    continue

                movie = Movie.objects.filter(imdb_id=data[0]).first()
                if not movie:
                    continue

                print(data)
                pm_data = {
                    "order": int(data[1]),
                    "category": data[3],
                    "job": data[4] if data[4] != "\\N" else "",
                    "characters": json.loads(data[5])
                    if not data[5].startswith("\\N")
                    else None,
                }

                PersonMovie.objects.get_or_create(
                    movie=movie, person=person, defaults=pm_data
                )