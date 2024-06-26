from django.shortcuts import get_object_or_404
from rest_framework import serializers
from club.serializers import LocationSerializer, MusicSerializer
from notifications.serializers import NotificationSerializer
from club.models import Location
from .models import User
from .google_register import register_social_user
from . import google

class UpdateUserSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(slug_field='slug', queryset=Location.objects.all())
    image = serializers.ImageField()
    class Meta:
        model = User
        fields = ['location', 'image']

class UserSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField(read_only=True)
    music = MusicSerializer(read_only=True, many=True)
    notifications = NotificationSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'first_name', 'password', 'first_name', 'last_name', 'type', 'location', 'music', 'type', 'notifications']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'allow_blank': False},
            'last_name': {'required': False,'allow_blank': False},
        }

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        type = validated_data['type']
        instance.type = type
        instance.save()
        return instance

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(request=self.context['request'],
            provider=provider, user_id=user_id, email=email, name=name)
