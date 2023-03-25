from django.contrib import admin
from .models import Music, Location, Type, Place, Event

# Register your models here.
admin.site.register(Music)
admin.site.register(Location)
admin.site.register(Type)
admin.site.register(Place)
admin.site.register(Event)
