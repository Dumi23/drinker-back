# Generated by Django 4.1.5 on 2023-06-15 15:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('club', '0011_place_latitude_place_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='followers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
