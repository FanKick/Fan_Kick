# views.py
from django.shortcuts import render
from apps.accounts.models import Player, Team
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.accounts.models import Player, Team
from apps.info.models import PlayerInfo, TeamInfo

def search_view(request):
    form = SearchForm(request.GET or None)
    players = []
    if form.is_valid():
        query = form.cleaned_data.get('query')
        players = Player.objects.filter(player_name__icontains=query)
    return render(request, 'search/search_results.html', {'form': form, 'players': players})

def player_detail_view(request, name=None):
    player = get_object_or_404(Player, player_name__iexact=name)
    return render(request, 'search/player_detail.html', {'player': player})

from django.http import JsonResponse
from apps.accounts.models import Player, Team
from apps.info.models import PlayerInfo, TeamInfo

def autocomplete(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(player_name__icontains=query)[:5]
    teams = Team.objects.filter(team_name__icontains=query)[:5]

    results = []
    for player in players:
        player_info = PlayerInfo.objects.filter(player=player).first()
        if player_info and player_info.info_player_name:
            player_name = player_info.info_player_name
        else:
            player_name = player.player_name
        
        # URL을 player_name으로 설정하고, player_info가 없으면 '/player/noone/'
        results.append({
            'name': player_name,
            'type': 'Player',
            'url': f'/player/{player_name}/' if player_info else '/player/noone/',
            'image': player.user.profile.url if player.user.profile else ''  # 프로필 이미지 URL 추가
        })

    for team in teams:
        team_info = TeamInfo.objects.filter(team=team).first()
        if team_info and team_info.info_team_name:
            team_name = team_info.info_team_name
        else:
            team_name = team.team_name
        
        # URL을 team_name으로 설정
        results.append({
            'name': team_name,
            'type': 'Team',
            'url': f'/team/{team_name}/',
            'image': team.team_picture.url if team.team_picture else ''  # 팀 이미지 URL 추가
        })

    return JsonResponse(results, safe=False)
