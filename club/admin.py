from django.contrib import admin
from .models import Music, Location, Type, Place

# Register your models here.
admin.site.register(Music)
admin.site.register(Location)
admin.site.register(Type)
admin.site.register(Place)