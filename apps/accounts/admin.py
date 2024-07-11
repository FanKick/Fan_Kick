from django.contrib import admin
from .models import CustomUser, Team, Player
from .forms import TeamForm, PlayerForm

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    exclude = ('last_login', 'first_name', 'last_name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    form = TeamForm
    list_display = ('team_name', 'created_at', 'updated_at')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    form = PlayerForm
    list_display = ('player_name', 'position', 'team', 'created_at', 'updated_at')
    list_filter = ('position', 'team')