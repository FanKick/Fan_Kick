from django.shortcuts import render, get_object_or_404
from .models import PlayerInfo, TeamInfo
from apps.accounts.models import Player

from django.shortcuts import render, get_object_or_404, redirect
from apps.accounts.models import Player

# info/views.py
from django.shortcuts import render, redirect
from apps.accounts.models import Player

def player_info_detail(request, info_player_name):
    try:
        player = Player.objects.get(info__info_player_name=info_player_name)
        return render(request, 'player_info_detail.html', {'player': player})
    except Player.DoesNotExist:
        return redirect('noone_info_detail')  # URL 이름을 사용한 리다이렉트
        # 또는
        # return redirect('/player/noone/')  # URL 경로를 사용한 리다이렉트


# def player_info_detail(request, info_player_name):
#     try:
#         player = Player.objects.get(info__info_player_name=info_player_name)
#     except Player.DoesNotExist:
#         return redirect('noone_info_detail')

#     return render(request, 'player_info_detail.html', {'player': player})

# def player_info_detail(request, info_player_name):
#     try:
#         player = get_object_or_404(PlayerInfo, info_info_player_name=info_player_name)
#         return render(request, 'player_info_detail.html', {'player': player})
#     except:
#         return redirect('info/noone_info_detail.html')

# def player_info_detail(request, info_player_name):
#     player = get_object_or_404(Player, info_player_name=info_player_name)
#     return render(request, 'player_info_detail.html', {'player': player})


def player_detail(request, info_player_name):
    # info_player_name을 사용하여 PlayerInfo 객체를 조회
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


def team_detail(request, info_team_name):
    # info_team_name을 사용하여 TeamInfo 객체를 조회
    team_info = get_object_or_404(TeamInfo.objects.select_related('team'), info_team_name=info_team_name)
    team = team_info.team

    # 모든 포지션의 선수 목록을 한 번에 가져오기
    players = Player.objects.filter(team=team).select_related('team')
    players_fw = players.filter(position='FW')
    players_mf = players.filter(position='MF')
    players_df = players.filter(position='DF')
    players_gk = players.filter(position='GK')

    context = {
        'team_info': team_info,
        'team': team,
        'players_fw': players_fw,
        'players_mf': players_mf,
        'players_df': players_df,
        'players_gk': players_gk,
    }

    return render(request, 'info/team_info_detail.html', context)
