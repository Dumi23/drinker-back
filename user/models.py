from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
# Create your models here.


class User(AbstractUser):    
    type_BASE_USER = 0
    type_OWNER = 1

    TYPE_CHOICES = (
        (type_BASE_USER, 'User'),
        (type_OWNER, 'Owner')
    ) 


    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    location = models.ForeignKey('club.Location', related_name="user_location", on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=500, validators= [MinLengthValidator(8)])
    type = models.IntegerField(choices=TYPE_CHOICES, null=True, default=0)
    email_verified = models.BooleanField(default=False)
    music = models.ManyToManyField('club.Music', related_name='user_music')
    notifications_disabled = models.BooleanField(default=False)
    notifications = models.ManyToManyField('notifications.Notification', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
