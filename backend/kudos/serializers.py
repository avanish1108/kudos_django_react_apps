# kudos/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Organization, UserProfile, Kudo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    available_kudos = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'organization', 'available_kudos']
    
    def get_available_kudos(self, obj):
        return obj.get_available_kudos()

class KudoSerializer(serializers.ModelSerializer):
    giver = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Kudo
        fields = ['id', 'giver', 'receiver', 'receiver_id', 'message', 'created_at']
        read_only_fields = ['id', 'giver', 'created_at']
    
    def create(self, validated_data):
        validated_data['giver'] = self.context['request'].user
        receiver_id = validated_data.pop('receiver_id')
        validated_data['receiver'] = User.objects.get(id=receiver_id)
        return super().create(validated_data)

class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user']