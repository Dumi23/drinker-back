# Generated by Django 4.1.5 on 2023-03-22 15:01

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0008_event_atendees_event_slug_alter_place_events_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='address',
        ),
        migrations.AddField(
            model_name='place',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AddField(
            model_name='place',
            name='street_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
