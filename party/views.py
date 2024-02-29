from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import HousePartySerializer
from .models import HouseParty
# Create your views here.


class CreateHouseParty(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = HousePartySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.created_by = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class UpdateHouseParty(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, slug): 
        party = get_object_or_404(HouseParty.objects.all(), slug=slug)
        if party.created_by != request.user:
            return Response({"message": "You have not created this party"}, status=status.HTTP_403_FORBIDDEN)
        serializer = HousePartySerializer(party, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class GetParty(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        party = get_object_or_404(HouseParty.objects.all(), slug=slug)
        if party.invites.filter(email=request.user.email).exists == False:
            return Response({"message": "You have not been invited to this party"}, status=status.HTTP_403_FORBIDDEN)
        serializer = HousePartySerializer(party)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteParty(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, slug):
        party = get_object_or_404(HouseParty.objects.all(), slug=slug)
        if party.created_by != request.user:
            return Response({"message": "You have not created this party"}, status=status.HTTP_403_FORBIDDEN)
        party.delete()
        return Response({"message": "Succesfuly deleted"}, status=status.HTTP_200_OK)