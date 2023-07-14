from django.db import models
from user.models import User
from drinker.utils import get_hashid
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        get_hashid(self, Type=Type, *args, **kwargs)
        

class Drink(models.Model):
    name = models.CharField(max_length=555, primary_key=True)

class Music(models.Model):
    genre = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True, editable=False)

    def __str__(self) -> str:
        return self.genre

    def save(self, *args, **kwargs):
        get_hashid(self, Type=Music, *args, **kwargs)
        

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_pics', null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=True, null=True)
    start_time = models.DateTimeField()
    atendees = models.ManyToManyField(User, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        get_hashid(self, Type=Event, *args, **kwargs)


class Location(models.Model):
    name = models.CharField(max_length=255)
    places = models.ManyToManyField('Place', related_name='location_places', blank=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        get_hashid(self, Type=Location, *args, **kwargs)

class Place(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False, null=True)
    owner = models.ForeignKey(User, related_name='owner_place', on_delete=models.DO_NOTHING, null=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='place_profile_pics/')
    is_active = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    location = models.ForeignKey(Location, related_name='place_location', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, related_name='place_type', on_delete=models.SET_NULL, null=True)
    events = models.ManyToManyField(Event, blank=True)
    upcoming_live_event = models.ForeignKey(Event, related_name='live_event', on_delete=models.SET_NULL, null=True, blank=True)
    music = models.ManyToManyField(Music)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    followers = models.ManyToManyField(User, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        get_hashid(self, Type=Place, *args, **kwargs)

class Socials(models.Model):
    id = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    facebook = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
