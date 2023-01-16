from django.urls import path
from .views import GetMusic, CreatePlace

urlpatterns = [
    path('music', GetMusic.as_view()),
    path('create', CreatePlace.as_view()),
]