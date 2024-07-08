from django.contrib import admin
from .models import CustomUser, Team, Player

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nickname', 'role')
    search_fields = ('username', 'email', 'nickname')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'created_at', 'updated_at')
    search_fields = ('team_name',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'position', 'team', 'created_at', 'updated_at')
    list_filter = ('position', 'team')
    search_fields = ('player_name', 'team__team_name')

