import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import PlaceSerializer, MusicSerializer, LocationSerializer, EventSerializer, TypeSerializer
from .models import *
# Create your views here.

class CreatePlace(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    def post(self, request):
        if request.user.type != User.type_OWNER:
            return Response({"message": "Your account type restricts you from making a place"})
        
        print(request.data)
        slug_music = request.data['slug_music[]']
        music_array = []
        music_array.append(slug_music)
        print(music_array)
        type = get_object_or_404(Type.objects.all(), slug=request.data['type'])
        image = request.data['image[]']
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(owner=request.user, type=type, image=image)            
            for i in music_array:
                try: 
                    print(i)
                    music = Music.objects.get(slug=i)
                    instance = Place.objects.latest('id')
                    instance.music.add(music)
                    instance.save()
                except Music.DoesNotExist:
                    pass
            serializer_dict = serializer.data
            location.places.add(instance)
            serializer_dict['message'] = "Place succesfully created. "
            print(serializer_dict)
            return Response(serializer_dict, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
class PlaceDetails(APIView):
    def get(self, request, slug):
        place = get_object_or_404(Place.objects.all(), slug=slug)
        serializer = PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EventDetails(APIView):
    def get(self, request, slug):
        event = get_object_or_404(Event.objects.all(), slug=slug)
        serializer = EventSerializer(event)
        if request.user.is_authenticated() == True:
            if event.atendees.filter(user=request.user).exists() == True:
                serializer_dict = serializer.data
                serializer_dict['attends_event'] = True
                return Response(serializer.data, status.HTTP_200_OK)
            else: 
                serializer_dict = serializer.data
                serializer_dict['attends_event'] = False   
                return Response(serializer.data, status.HTTP_200_OK)         
        return Response(serializer.data, status.HTTP_200_OK)
        
class UpdatePlace(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, slug):
        place = get_object_or_404(Place.objects.all(), slug=slug)
        if place.owner != request.user:
            return Response({"error": "You are not the owner of this locale"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PlaceSerializer(place, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer_one = PlaceSerializer(instance=place)
            serializer_dict = serializer_one.data
            serializer_dict['message'] = "Locale updated successfuly"
            return Response(serializer_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateEvent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        place = get_object_or_404(Place.objects.all(), slug=slug)
        if place.owner != request.user:
            return Response({"error": "You are not the owner of this locale"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = EventSerializer(request.data)
        if serializer.is_valid():
            event = serializer.save()
            place.events.add(event)
            place.upcoming_live_event = event
            place.save
            serializer_dict = serializer.data
            serializer_dict['message'] = "Event successfuly created"
            return Response(serializer_dict, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
class UpdateEvent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, slug, slug_ev):
        place = get_object_or_404(Place.objects.all(), slug=slug)
        if place.owner != request.user:
            return Response({"error": "You are not the owner of this locale"}, status=status.HTTP_401_UNAUTHORIZED)
        event = get_object_or_404(Event.objects.all(), slug=slug_ev)
        serializer = EventSerializer(event, request.data)
        if serializer.is_valid():
            serializer.save()
            serializer_one = EventSerializer(instance=event)
            serializer_dict = serializer_one.data
            serializer_dict['message'] = "Event updated successfuly"
            return Response(serializer_dict, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class UnauthedUserFeed(ListAPIView):
    def get(self, request):
        queryset = Place.objects.all()
        paginate = self.paginate_queryset(queryset)
        serializer = PlaceSerializer(paginate, many=True)
        return self.get_paginated_response(serializer.data)
    
class UnauthedUserEventFeed(ListAPIView):
    def get(self, reuqest):
        queryset = Place.objects.all().values('events')
        paginate = self.paginate_queryset(queryset)
        serializer = EventSerializer(paginate, many=True)
        return self.get_paginated_response(serializer.data)


class UserFeed(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        if self.request.user.is_authenticated == True:
            values = self.request.user.music.all().values('id')
            value_list = []
            for i in values:
                value_list.append(i['id'])
            print(value_list)
            queryset = Place.objects.filter(location=self.request.user.location, music__in = value_list).all().distinct()  
            return queryset
        else:
            queryset = Place.objects.all()  
            return queryset
        
class UserEventFeed(ListAPIView):
    serializer_class = PlaceSerializer
    pagination_class = PageNumberPagination
    def get(self, request):
        if request.user.is_authenticated == True:
            following = request.data['following']  
            values = request.user.music.all().values('id')
            value_list = []
            for i in values:
                value_list.append(i['id'])
            queryset = Place.objects.filter(location=request.user.location, music__in=value_list).distinct()
            event_qs = Event.objects.filter(place__in=queryset, start_time__lte=datetime.datetime.now(), start_time__gt=datetime.datetime.today() - datetime.timedelta(days=30)).distinct()
            paginate = self.paginate_queryset(queryset=event_qs)
            serializer = EventSerializer(paginate, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            queryset = Event.objects.filter(start_time__lte=datetime.datetime.now(), start_time__gt=datetime.datetime.today() - datetime.timedelta(days=30))
            paginate = self.paginate_queryset(queryset)
            serializer = EventSerializer(paginate, many=True)
            return self.get_paginated_response(serializer.data)

class GetMusic(APIView):
    queryset = Music.objects.all().order_by('-id').distinct()
    serializer_class = MusicSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^genre']
    def get(self, request):
        serializer = MusicSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)

class GetLocations(ListAPIView):
    queryset = Location.objects.all().order_by('-id').distinct()
    serializer_class = LocationSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^name']
    def get_queryset(self):
        return self.queryset.distinct()
    
class GetTypes(ListAPIView):
    queryset = Type.objects.all().order_by('-id').distinct()
    serializer_class = TypeSerializer
    def get_queryset(self):
        return self.queryset.distinct()
    

class AttendEvent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        event = get_object_or_404(Event.objects.all(), slug=slug)
        event.atendees.add(request.user)
        return Response({"message": "Will attend event"}, status.HTTP_200_OK)
    
class RemoveAttendanceForEvent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        event = get_object_or_404(Event.objects.all(), slug=slug)
        if event.atendees.filter(email=request.user.email).exists() == True:
            event.atendees.remove(request.user)
            return Response({"message": "Will not attend event anymore"}, status.HTTP_200_OK)
        return Response({"message": "You have not marked this event for attendance"}, status.HTTP_400_BAD_REQUEST)
    
class FollowPlace(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        place = get_object_or_404(Place.objects.all(), slug=slug)
        place.followers.add(request.user)
        return Response({"message": "Followed place"}, status=status.HTTP_200_OK)
    
class UnfollowPlace(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        place = get_object_or_404(Place.objects.all(), slug=slug)
        if place.followers.filter(email=request.user.email).exists() == True:
            place.followers.remove(request.user)
            return Response({"message": "Unfollowed place"}, status=status.HTTP_200_OK) 
        return Response({"message": "You have not followed this place"}, status=status.HTTP_400_BAD_REQUEST)
    
