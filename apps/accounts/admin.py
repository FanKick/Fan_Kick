from django.contrib import admin
from .models import CustomUser, Team, Player

# CustomUser 모델 등록
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_player', 'is_team', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'nickname')
    list_filter = ('role', 'is_player', 'is_team')

# Team 모델 등록
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'user', 'created_at', 'updated_at')
    search_fields = ('team_name',)
    list_filter = ('created_at', 'updated_at')

# Player 모델 등록
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'position', 'team', 'birthday', 'created_at', 'updated_at')
    search_fields = ('player_name', 'position')
    list_filter = ('team', 'created_at', 'updated_at')
