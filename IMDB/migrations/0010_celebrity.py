# Generated by Django 3.2.7 on 2021-10-04 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IMDB', '0009_auto_20210928_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Celebrity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='celebrities')),
            ],
        ),
    ]
