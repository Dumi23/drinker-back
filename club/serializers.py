from rest_framework import serializers
from .models import *

class TypeSerializer(serializers.Serializer):
    class Meta:
        model = Type
        fields = ['name']

class DrinkSerializer(serializers.Serializer):
    class Meta:
        model = Drink
        fields = ['name']

class MusicSerializer(serializers.Serializer):
    class Meta:
        model = Music
        fields = ['genre']

class EventSerializer(serializers.Serializer):
    class Meta:
        model = Event
        fields = ['name', 'description', 'is_active', 'start_time']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'start_time': {'required': True}
        }


        def create(self, validated_data):
            instance = Event(**validated_data)
            instance.save()
            return instance


class LocationSerializer(serializers.Serializer):
    class Meta:
        model = Location
        fields = ['city_name', 'street_name', 'street_number']
        extra_kwargs = {
            'city_name': {'required': True},
            'street_name': {'required': True},
            'stret_number': {'required': True}
        }

    def create(self, validated_data):
        instance = Location(**validated_data)
        instance.save()
        return instance

class PlaceSerializer(serializers.Serializer):
    location = LocationSerializer(read_only=True)
    type = TypeSerializer(read_only=True)
    events = EventSerializer(read_only=True, many=True)
    upcoming_live_event = EventSerializer(read_only=True)
    class Meta:
        model = Place
        fields = ['name', 'description', 'is_active', 'is_validated', 'location', 'type', 'events', 'upcoming_live_event']

