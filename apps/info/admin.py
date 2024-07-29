from django.contrib import admin
from .models import TeamInfo
from .models import PlayerInfo

@admin.register(PlayerInfo)
class PlayerInfoAdmin(admin.ModelAdmin):
    list_display = ('player', 'info_player_name', 'player_picture')
    search_fields = ('player__player_name', 'info_player_name')

@admin.register(TeamInfo)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ('team', 'info_team_name')