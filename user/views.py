from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.backends import TokenBackend
from .models import User
from .serializers import UserSerializer, GoogleSocialAuthSerializer
from django.urls import reverse
from .utils import Util
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.latest('id')
        token = AccessToken.for_user(user)
        print(user.email)
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
