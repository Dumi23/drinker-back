from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializers import PlaceSerializer, MusicSerializer, LocationSerializer
from .models import *
# Create your views here.

class CreatePlace(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.type != User.type_OWNER:
            return Response({"message": "Your account type restricts you from making a place"})
        
        slug_music = request.data['slug_music']
        music_array = slug_music
        print(music_array)
        location = get_object_or_404(Location.objects.all(), slug=request.data['location_slug'])
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(owner=request.user, location=location)            
            for i in music_array:
                try: 
                    music = Music.objects.get(slug=i)
                    instance = Place.objects.latest('-id')
                    instance.music.add(music)
                    instance.save()
                except Music.DoesNotExist:
                    pass
            serializer_dict = serializer.data
            location.places.add(instance)
            serializer_dict['message'] = "Place succesfully created. "
            return Response(serializer_dict, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class UserFeed(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer
    pagination_class = PageNumberPagination
    def get(self, request):
        values = request.user.music.all().values('id')
        value_list = []
        for i in values:
            value_list.append(i['id'])
        print(value_list)
        queryset = Place.objects.filter(location=request.user.location, music__in = value_list).distinct()  
        paginate = self.paginate_queryset(queryset)
        serializer = PlaceSerializer(paginate, many=True)
        return self.get_paginated_response(serializer.data)
        

class GetMusic(ListAPIView):
    queryset = Music.objects.all().order_by('-id').distinct()
    serializer_class = MusicSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^genre']
    def get_queryset(self):
        return self.queryset.distinct()

class GetLocations(ListAPIView):
    queryset = Location.objects.all().order_by('-id').distinct()
    serializer_class = LocationSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^name']
    def get_queryset(self):
        return self.queryset.distinct()