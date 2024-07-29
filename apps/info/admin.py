from django.contrib import admin
from .models import TeamInfo

@admin.register(TeamInfo)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_name_search', 'created_at', 'updated_at')
    search_fields = ('team_name', 'team_name_search')
    prepopulated_fields = {'team_name_search': ('team_name',)}  # team_name을 기반으로 team_name_search 필드 자동 생성
