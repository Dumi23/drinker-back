from django.shortcuts import render
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
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            serializer_dict = serializer.data
            serializer_dict['message'] = "Place succesfully created. "
            for i in slug_music:
                try: 
                    music = Music.objects.get(slug=i)
                    instance = Place.objects.latest('-id')
                    instance.music.add(music)
                    instance.save()
                except Music.DoesNotExist:
                    pass
            return Response(serializer_dict, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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