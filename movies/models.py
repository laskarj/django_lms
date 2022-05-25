from django.db import models
from django.contrib.postgres.fields import ArrayField


class Movie(models.Model):
    MOVIE = 'movie'
    SHORT = 'short'
    TITLE_TYPE = [
        (MOVIE, 'Movie'),
        (SHORT, 'Short')
    ]
    imdb_id = models.CharField(primary_key=True, max_length=255)
    title_type = models.CharField(max_length=255, choices=TITLE_TYPE)
    name = models.CharField(max_length=255)
    is_adult = models.BooleanField()
    year = models.DateTimeField(null=True)
    genres = ArrayField(models.CharField(max_length=255), default=list)

    def __str__(self):
        return self.name


class Person(models.Model):
    imdb_id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    birth_year = models.DateField(null=True)
    death_year = models.DateField(null=True)

    def __str__(self):
        return self.name


class PersonMovie(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    order = models.IntegerField()
    category = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    characters = ArrayField(models.CharField(max_length=255), null=True)
