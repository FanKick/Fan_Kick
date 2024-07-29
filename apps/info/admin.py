from django.contrib import admin
from .models import TeamInfo

@admin.register(TeamInfo)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ('team', 'info_team_name')