# views.py
from django.shortcuts import render
from apps.accounts.models import Player, Team
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.accounts.models import Player, Team

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



def autocomplete(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(player_name__icontains=query)[:5]
    teams = Team.objects.filter(team_name__icontains=query)[:5]

    results = []
    for player in players:
        results.append({
            'name': player.player_name,
            'type': 'Player',
            'url': f'/{player.id}/player',
            'image': player.user.profile.url if player.user.profile else ''  # 프로필 이미지 URL 추가
        })

    for team in teams:
        results.append({
            'name': team.team_name,
            'type': 'Team',
            'url': f'/{team.id}/team',
            'image': team.team_picture.url if team.team_picture else ''  # 팀 이미지 URL 추가
        })

    return JsonResponse(results, safe=False)