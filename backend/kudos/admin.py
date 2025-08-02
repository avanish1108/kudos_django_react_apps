# kudos/admin.py
from django.contrib import admin
from .models import Organization, UserProfile, Kudo

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization']
    list_filter = ['organization']

@admin.register(Kudo)
class KudoAdmin(admin.ModelAdmin):
    list_display = ['giver', 'receiver', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['giver__username', 'receiver__username', 'message']
