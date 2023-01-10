from django.db import models

# Create your models here.
class Drink(models.Model):
    name = models.CharField(max_length=555, primary_key=True)

class Music(models.Model):
    genre = models.CharField(max_length=255, primary_key=True)

    def __str__(self) -> str:
        return self.genre

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField()