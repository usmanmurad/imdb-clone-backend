# Generated by Django 3.2.7 on 2021-10-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IMDB', '0010_celebrity'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]