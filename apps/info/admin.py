from django.contrib import admin
from .models import TeamInfo

@admin.register(TeamInfo)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'created_at', 'updated_at')
    search_fields = ('team_name',)