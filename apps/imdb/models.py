from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.db import models

User = get_user_model()


class Movie(models.Model):
    class TitleType(models.TextChoices):
        SHORT = 'short', _('Short')
        MOVIE = 'movie', _('Movie')

    imdb_id = models.CharField(_('IMDB id'), max_length=255, null=True)
    title_type = models.CharField(_('Type of the title'), max_length=255, choices=TitleType.choices)
    name = models.CharField(_('Name'), max_length=255)
    is_adult = models.BooleanField(_('Is Adult'))
    date = models.DateField(_('Release Date'), null=True)
    genres = ArrayField(models.CharField(max_length=255), verbose_name=_('Genres'))


class Person(models.Model):
    imdb_id = models.CharField(_('IMDB id'), max_length=255, null=True)
    name = models.CharField(_('Name'), max_length=255)
    birth_date = models.DateField(_('Birth Date'), null=True)
    death_date = models.DateField(_('Death Date'), null=True)
    movies = models.ManyToManyField(Movie, through='PersonMovie')


class PersonMovie(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    order = models.IntegerField(_('Ordering'))
    category = models.CharField(_('Category'), max_length=255)
    job = models.CharField(_('Job'), max_length=255)
    characters = ArrayField(models.CharField(max_length=255), verbose_name=_('Characters'), null=True)
