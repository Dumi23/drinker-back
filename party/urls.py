from django.urls import path
from .views import *




urlpatterns = [
    path('create', CreateHouseParty.as_view()),
    path('update/<str:slug>', UpdateHouseParty.as_view()),
    path('<str:slug>', GetParty.as_view()),
    path('delete/<str:slug>', DeleteParty.as_view())
]