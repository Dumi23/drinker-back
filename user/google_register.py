from django.contrib.auth import authenticate
from django.http import request
from .models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.utils.decorators import method_decorator

def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)

def register_social_user(request, provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)
    
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            try:
                registered_user = authenticate(request=request,
                    email=email, password=os.environ.get('SOCIAL_SECRET'))
            except AuthenticationFailed:
                return {
                    "message": "credentials not valid"
                }

            return {
                'username': filtered_user_by_email[0].username,
                'email': filtered_user_by_email[0].email,
                'token': str(AccessToken.for_user(filtered_user_by_email[0])),
                'refresh': str(RefreshToken.for_user(filtered_user_by_email[0]))}

        else:
            return {
                "message" : "Please login with your user credentials since your account alreday exists"
            }

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        try:
            new_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))
        except AuthenticationFailed:
            return {
                "message": "Credentials not valid"
            }

        return {
            'email': user.email,
            'username': user.username,
            'token': str(AccessToken.for_user(user)),
            'refresh': str(AccessToken.for_user(user))
        }