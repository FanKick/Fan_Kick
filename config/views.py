from django.shortcuts import render
from apps.accounts.models import Team, Player, Membership
from apps.info.models import TeamInfo

def home(request):
    user = request.user
    teams = Team.objects.all()
    # teaminfos = TeamInfo.objects.all()
    teaminfos = TeamInfo.objects.select_related('team').all()

    players = Player.objects.select_related('user', 'team').all()

    if user.is_authenticated:
        memberships = Membership.objects.filter(user=user, is_active=True).select_related('team')
    else:
        memberships = None

    context = {
        'teams': teams,
        'memberships': memberships,
        'players' : players,
        'teaminfos': teaminfos,
    }


    return render(request, 'home.html', context)