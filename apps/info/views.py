# apps/info/views.py

from django.shortcuts import render, get_object_or_404
from apps.accounts.models import Team, Player
from .models import TeamInfo

def team_info_detail(request, pk):
    team_info = get_object_or_404(TeamInfo, team__pk=pk)
    players_fw = Player.objects.filter(team=team_info.team, position='FW')
    players_mf = Player.objects.filter(team=team_info.team, position='MF')
    players_df = Player.objects.filter(team=team_info.team, position='DF')
    players_gk = Player.objects.filter(team=team_info.team, position='GK')
    return render(request, 'info/team_info_detail.html', {
        'team_info': team_info,
        'players_fw': players_fw,
        'players_mf': players_mf,
        'players_df': players_df,
        'players_gk': players_gk,
    })


from django.shortcuts import render, get_object_or_404
from apps.accounts.models import Team, Player
from .models import TeamInfo

def team_info_detail(request, pk):
    team_info = get_object_or_404(TeamInfo, team__pk=pk)
    players_fw = Player.objects.filter(team=team_info.team, position='FW')
    players_mf = Player.objects.filter(team=team_info.team, position='MF')
    players_df = Player.objects.filter(team=team_info.team, position='DF')
    players_gk = Player.objects.filter(team=team_info.team, position='GK')
    return render(request, 'info/team_info_detail.html', {
        'team_info': team_info,
        'team': team_info.team,
        'players_fw': players_fw,
        'players_mf': players_mf,
        'players_df': players_df,
        'players_gk': players_gk,
    })
