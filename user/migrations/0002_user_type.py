# Generated by Django 4.1.5 on 2023-01-16 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.IntegerField(choices=[(0, 'User'), (1, 'Owner')], default=0, null=True),
        ),
    ]
