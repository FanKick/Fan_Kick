# apps/info/views.py

from django.shortcuts import render, get_object_or_404
from apps.accounts.models import Player, Team
from .models import TeamInfo

def team_info_by_team_name_search(request, team_name_search):
    team_info = get_object_or_404(TeamInfo, team_name_search=team_name_search)
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


# def team_info_by_team_name_search(request, team_name_search):
#     team_info = get_object_or_404(TeamInfo, team_name_search=team_name_search)
#     return render(request, 'info/team_info_detail.html', {'team_info': team_info, 'team': team_info.team})

def team_info_by_player_name(request, player_name_search):
    player = get_object_or_404(Player, player_name__iexact=player_name_search)
    team_info = get_object_or_404(TeamInfo, team=player.team)
    return render(request, 'info/team_info_detail.html', {'team_info': team_info, 'team': team_info.team})


def team_info_by_team_name(request, team_name):
    # team_name을 통해 해당 팀을 찾습니다.
    team = get_object_or_404(Team, team_name__iexact=team_name)
    # 팀 정보를 가져옵니다.
    team_info = get_object_or_404(TeamInfo, team=team)
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

# def team_info_by_player_name(request, player_name):
#     # player_name을 통해 해당 플레이어를 찾습니다.
#     player = get_object_or_404(Player, player_name__iexact=player_name)
#     # 플레이어의 팀 정보를 가져옵니다.
#     team_info = get_object_or_404(TeamInfo, team=player.team)
#     players_fw = Player.objects.filter(team=team_info.team, position='FW')
#     players_mf = Player.objects.filter(team=team_info.team, position='MF')
#     players_df = Player.objects.filter(team=team_info.team, position='DF')
#     players_gk = Player.objects.filter(team=team_info.team, position='GK')
#     return render(request, 'info/team_info_detail.html', {
#         'team_info': team_info,
#         'team': team_info.team,
#         'players_fw': players_fw,
#         'players_mf': players_mf,
#         'players_df': players_df,
#         'players_gk': players_gk,
#     })


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
