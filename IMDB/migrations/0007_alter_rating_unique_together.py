# Generated by Django 3.2.7 on 2021-09-22 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMDB', '0006_alter_rating_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user', 'movie')},
        ),
    ]
