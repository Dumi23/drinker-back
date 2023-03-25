from django.urls import path
from .views import (GetMusic, CreatePlace, GetLocations, UserFeed, PlaceDetails, 
    EventDetails, CreateEvent, UpdatePlace, UnauthedUserEventFeed, UnauthedUserFeed, UserEventFeed, UpdateEvent)

urlpatterns = [
    path('music', GetMusic.as_view()),
    path('locale/create', CreatePlace.as_view()),
    path('location', GetLocations.as_view()),
    path('feed', UserFeed.as_view()),
    path('locale/<str:slug>', PlaceDetails.as_view()),
    path('locale/update/<str:slug>', UpdatePlace.as_view()),
    path('locale/<str:slug>/event', CreateEvent.as_view()),
    path('locale/<str:slug>/event/<str:slug_ev>', UpdateEvent.as_view()),
    path('event/<str:slug>', EventDetails.as_view())
]