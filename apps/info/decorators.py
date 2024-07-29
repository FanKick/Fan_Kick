from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Membership

def membership_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        if not team_id:
            return redirect('some_error_page')  # 팀 ID가 없을 경우 처리

        membership = Membership.objects.filter(user=request.user, team_id=team_id, is_active=True).exists()
        if not membership:
            return redirect('membership_required_page')  # 가입이 필요한 페이지로 리디렉션

        return view_func(request, *args, **kwargs)
    return _wrapped_view
