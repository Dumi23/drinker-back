from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PlaceSerializer, MusicSerializer
from .models import *
# Create your views here.

class CreatePlace(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.type != User.type_OWNER:
            return Response({"message": "Your account type restricts you from making a place"})
        
        slug_music = request.data['slug']
        serializer = PlaceSerializer(data=request.data)

class GetMusic(ListAPIView):
    queryset = Music.objects.all().order_by('-id').distinct()
    serializer_class = MusicSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^genre']
    def get_queryset(self):
        return self.queryset.distinct()
