import os.path

from django.core.management.base import BaseCommand

from apps.imdb.models import Movie


class Command(BaseCommand):
    help = "Imorts movies from tsv file"

    def add_arguments(self, parser):
        parser.add_argument("-F", "--file", type=str, required=True)

    def handle(self, *args, **options):
        file_name = options.get("file")

        if not os.path.exists(file_name):
            print("No file exists.")

        with open(file_name, encoding="utf-8") as f:
            for line in f.readlines():
                if not line:
                    continue

                if not line.startswith("tt"):
                    continue
                data = line.split("\t")

                if data[1] not in ("movie", "short"):
                    continue

                date = data[5]
                if date == "\\N":
                    date = None
                else:
                    date = f"{date}-01-01"

                movie_data = {
                    "title_type": data[1],
                    "name": data[2],
                    "is_adult": data[4] == "1",
                    "date": date,
                    "genres": data[8].split(","),
                }
                movie, created = Movie.objects.get_or_create(
                    imdb_id=data[0], defaults=movie_data
                )

                if created:
                    Movie.objects.filter(id=movie.id).update(**movie_data)
