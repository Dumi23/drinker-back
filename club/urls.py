from django.urls import path
from .views import (GetMusic, CreatePlace, GetLocations, UserFeed, PlaceDetails, 
    EventDetails, CreateEvent, UpdatePlace, UserEventFeed, UpdateEvent, GetTypes,
    AttendEvent, RemoveAttendanceForEvent, FollowPlace, UnfollowPlace)

urlpatterns = [
    path('music', GetMusic.as_view()),
    path('locale/create', CreatePlace.as_view()),
    path('location', GetLocations.as_view()),
    path('feed', UserFeed.as_view()),
    path('locale/<str:slug>', PlaceDetails.as_view()),
    path('locale/update/<str:slug>', UpdatePlace.as_view()),
    path('locale/<str:slug>/event', CreateEvent.as_view()),
    path('locale/<str:slug>/event/<str:slug_ev>', UpdateEvent.as_view()),
    path('event/<str:slug>', EventDetails.as_view()),
    path('types', GetTypes.as_view()),
    path('event/attend/<str:slug>', AttendEvent.as_view()),
    path('event/unattend/<str:slug>', RemoveAttendanceForEvent.as_view()),
    path('events', UserEventFeed.as_view()),
    path('locale/follow/<str:slug>', FollowPlace.as_view()),
    path('locale/unfollow/<str:slug>', UnfollowPlace.as_view()),
]