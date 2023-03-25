from rest_framework import serializers
from .models import *

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['name']

class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['name']

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['genre', 'slug']

class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Event
        fields = ['name', 'description', 'image' ,'slug' ,'is_active', 'start_time']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'start_time': {'required': True},
            'slug': {'required': False},
        }


        def create(self, validated_data):
            instance = Event(**validated_data)
            instance.save()
            return instance

class PlaceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    location = serializers.StringRelatedField(read_only=True)
    type = TypeSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_validated = serializers.BooleanField(read_only=True)
    events = EventSerializer(read_only=True, many=True)
    upcoming_live_event = EventSerializer(read_only=True)
    music = MusicSerializer(read_only=True, many=True)
    class Meta:
        model = Place
        fields = ['name', 'description', 'slug' ,'is_active', 'is_validated', 'location' , 'type', 'events', 'upcoming_live_event', 'image', 'music', 'street_name', 'phone_number']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
        }

        def create(self, validated_data):
            instance = Place(**validated_data)
            instance.save()
            return instance

class LocationSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(read_only=True, many=True)
    class Meta:
        model = Location
        fields = ['name', 'slug', 'places']