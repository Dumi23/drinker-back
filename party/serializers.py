from rest_framework import serializers
from club.serializers import AtendeeSerializer
from .models import HouseParty

class HousePartySerializer(serializers.ModelSerializer):
    start_time_and_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    created_by = AtendeeSerializer(many=False, read_only=True)
    invites = AtendeeSerializer(many=True, read_only=False)
    class Meta:
        model = HouseParty
        fields = ['name', 'slug', 'start_time_and_date', 'invites', 'location']
