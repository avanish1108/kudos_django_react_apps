# kudos/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Organization(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"
    
    def get_available_kudos(self):
        """Calculate available kudos for the current week"""
        week_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        given_this_week = Kudo.objects.filter(
            giver=self.user,
            created_at__gte=week_start
        ).count()
        
        return max(0, 3 - given_this_week)

class Kudo(models.Model):
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_kudos')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_kudos')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.giver.username} -> {self.receiver.username}: {self.message[:50]}"
