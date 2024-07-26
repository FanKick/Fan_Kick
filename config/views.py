from django.shortcuts import render
from apps.accounts.models import Team, Membership
from apps.info.models import TeamInfo

def home(request):
    user = request.user
    teams = Team.objects.all()
    teaminfos = TeamInfo.objects.all()

    if user.is_authenticated:
        memberships = Membership.objects.filter(user=user, is_active=True).select_related('team')
    else:
        memberships = []

    context = {
        'teams': teams,
        'teaminfos': teaminfos,
        'memberships': memberships,
    }


    return render(request, 'home.html', context)