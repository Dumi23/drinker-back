from django.urls import path
from .views import GetMusic, CreatePlace, GetLocations, UserFeed

urlpatterns = [
    path('music', GetMusic.as_view()),
    path('create', CreatePlace.as_view()),
    path('location', GetLocations.as_view()),
    path('feed', UserFeed.as_view()),
]