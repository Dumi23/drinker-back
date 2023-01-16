from django.urls import path
from .views import GetMusic

urlpatterns = [
    path('music', GetMusic.as_view())
]