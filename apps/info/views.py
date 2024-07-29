from django.shortcuts import render, get_object_or_404
from apps.info.models import TeamInfo
from apps.accounts.models import Player

from django.shortcuts import render, get_object_or_404
from .models import PlayerInfo

def player_detail(request, info_player_name):
    player_info = get_object_or_404(PlayerInfo, info_player_name=info_player_name)
    player = player_info.player
    team_info = player.team.team_info

    context = {
        'player': player,
        'player_info': player_info,
        'team': player.team,
        'team_info': team_info,
    }
    return render(request, 'info/player_info_detail.html', context)


def team_info_by_info_team_name(request, info_team_name):
    # team_name_search 값을 기반으로 TeamInfo 객체를 조회
    team_info = get_object_or_404(TeamInfo, info_team_name=info_team_name)
    team = team_info.team

    # 포지션별 선수 목록 가져오기
    players_fw = Player.objects.filter(team=team, position='FW')
    players_mf = Player.objects.filter(team=team, position='MF')
    players_df = Player.objects.filter(team=team, position='DF')
    players_gk = Player.objects.filter(team=team, position='GK')

    context = {
        'team_info': team_info,
        'team': team,
        'players_fw': players_fw,
        'players_mf': players_mf,
        'players_df': players_df,
        'players_gk': players_gk,
    }

    return render(request, 'info/team_info_detail.html', context)