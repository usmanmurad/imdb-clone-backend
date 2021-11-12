from django.db import models
from django.contrib.auth.models import AbstractUser
from django_better_admin_arrayfield.models.fields import ArrayField


class User(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    watchlist = ArrayField(models.IntegerField(), default=list, blank=True)


class Movie(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='posters', blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)
    director = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    cast = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    genre = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    average_rating = models.FloatField(blank=True)
    number_of_reviews = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    trailer_id = models.CharField(max_length=50, blank=True)


class Rating(models.Model):
    rating = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')


class Celebrity(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='celebrities', blank=True)
