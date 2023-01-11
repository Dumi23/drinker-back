from django.db import models

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=255)

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

    def __str__(self) -> str:
        return self.name

class Location(models.Model):
    city_name = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)


class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(storage='place_profile_pics')
    is_active = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    location = models.ForeignKey(Location, related_name='place_location', on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, related_name='place_type', on_delete=models.DO_NOTHING)
    events = models.ManyToManyField(Event)

class Socials(models.Model):
    id = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    facebook = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)