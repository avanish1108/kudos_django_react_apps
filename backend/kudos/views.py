# kudos/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from .models import Organization, UserProfile, Kudo
from .serializers import (
    UserProfileSerializer, KudoSerializer, TeamMemberSerializer
)

@api_view(['POST'])
@permission_classes([])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})

@api_view(['GET'])
def current_user(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

class TeamMembersListView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer
    
    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return UserProfile.objects.filter(
            organization=user_profile.organization
        ).exclude(user=self.request.user)

class KudoCreateView(generics.CreateAPIView):
    serializer_class = KudoSerializer
    
    def create(self, request, *args, **kwargs):
        # Check if user has available kudos
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.get_available_kudos() <= 0:
            return Response(
                {'error': 'No kudos available this week'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if trying to give kudo to self
        receiver_id = request.data.get('receiver_id')
        if receiver_id == request.user.id:
            return Response(
                {'error': 'Cannot give kudos to yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if receiver is in same organization
        try:
            receiver_profile = UserProfile.objects.get(user_id=receiver_id)
            user_profile = UserProfile.objects.get(user=request.user)
            if receiver_profile.organization != user_profile.organization:
                return Response(
                    {'error': 'Can only give kudos to users in your organization'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Receiver not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)

class ReceivedKudosListView(generics.ListAPIView):
    serializer_class = KudoSerializer
    
    def get_queryset(self):
        return Kudo.objects.filter(receiver=self.request.user)

class GivenKudosListView(generics.ListAPIView):
    serializer_class = KudoSerializer
    
    def get_queryset(self):
        return Kudo.objects.filter(giver=self.request.user)