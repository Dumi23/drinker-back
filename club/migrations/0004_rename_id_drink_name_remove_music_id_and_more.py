# Generated by Django 4.1.5 on 2023-01-10 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_remove_drink_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drink',
            old_name='id',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='music',
            name='id',
        ),
        migrations.AlterField(
            model_name='music',
            name='genre',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]