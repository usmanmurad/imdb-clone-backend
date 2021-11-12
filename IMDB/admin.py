from django.contrib import admin
from IMDB.models import User, Movie, Rating, Celebrity
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


class AdminMovie(admin.ModelAdmin, DynamicArrayMixin):
    pass


admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Movie, AdminMovie)
admin.site.register(Celebrity)
