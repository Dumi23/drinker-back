from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.backends import TokenBackend
from .models import User
from club.models import Location, Music
from .serializers import UserSerializer, GoogleSocialAuthSerializer, UpdateUserSerializer
from django.urls import reverse
from .utils import Util
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from club.serializers import PlaceSerializer
from club.models import Place

# Create your views here.

class EmailVerify(APIView):
    def get(self, request, token):
        if not token:
            return Response({"message":"Unauthenticated"}, status.HTTP_403_FORBIDDEN)
        user_token = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = user_token['user_id']
        user = User.objects.get(id=user_id)
        user.email_verified = True 
        user.save()
        return Response("Email successfully verified.")    

class Register(APIView):
    def post(self, request, *args, **kwargs):
        music_slug = request.data['music_slug']
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.latest('id')
        token = AccessToken.for_user(user)
        for i in music_slug:
            try: 
                music = Music.objects.get(slug=i)
                user.music.add(music)
            except Music.DoesNotExist:
                pass
        relativeLink = reverse('email-verify', kwargs={'token': token})
        current_site = get_current_site(request=request).domain
        absurl = 'http://' + current_site + relativeLink
        email_body = 'Hi ' + user.username +' Use this link to verify your email \n' + absurl
        data = {'email_body': email_body, 'email': user.email, 'email_subject': 'Email Verification'}
        serializer_one = UserSerializer(user)
        serializer_dict = serializer_one.data
        serializer_dict['message'] = 'Please verify your account with the link that was sent to your email.'
        Util.send_email(data)
        return Response(serializer_dict, status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            return Response({'message': 'User does not exist'}, status.HTTP_404_NOT_FOUND)
        
        if user.email_verified == False:
            return Response({'message': 'Email is not verified'}, status.HTTP_403_FORBIDDEN)
        
        if not user.check_password(password):
            return Response({"message": "Incorrect Password"}, status.HTTP_403_FORBIDDEN)

        token = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)



        serializer = UserSerializer(user)
        serializer_dict = serializer.data
        serializer_dict['token'] = str(token)
        serializer_dict['refresh'] = str(refresh)

        response = Response(serializer_dict, status.HTTP_200_OK)
        response.set_cookie(key='refresh', value=refresh, httponly=True)

        return response


class Google(APIView):
    serializer_class = GoogleSocialAuthSerializer
    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(context={'request': request},data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)    


class Logout(APIView):
    quersey = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        blacklist = RefreshToken(request.COOKIES.get('refresh'))
        blacklist.blacklist()
        response = Response({'message': 'Successful Logout'})
        response.set_cookie(key='refresh', value='', httponly=True)    
        return response  


class Me(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        place_queryset = Place.objects.filter(owner=user).distinct()
        paginate = self.paginate_queryset(place_queryset)
        paginated_serializer = PlaceSerializer(paginate, many=True)
        response = self.get_paginated_response(paginated_serializer.data)
        response.data['user_data'] = serializer.data
        return response
    
class UpdateUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer_update = UpdateUserSerializer(request.user, request.data ,partial=True)
        if serializer_update.is_valid(raise_exception=True):
            serializer_update.save()
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ClearNotifications(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.notifications.clear()
        return Response({"message": "Cleared Notifications"}, status=status.HTTP_200_OK)