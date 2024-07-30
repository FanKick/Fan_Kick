from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Subscription
from apps.accounts.models import Player
from apps.payments.models import SubscriptionPayment
from apps.payments.services import cancel_scheduled_payment
from django.http import JsonResponse

@login_required
def subscription_management(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'active':
        subscriptions_list = Subscription.objects.filter(subscriber=request.user, status=True).order_by('-start_date')
    else:
        subscriptions_list = Subscription.objects.filter(subscriber=request.user).order_by('-start_date')
    
    paginator = Paginator(subscriptions_list, 5)  # 페이지당 5개 항목
    page_number = request.GET.get('page')
    subscriptions = paginator.get_page(page_number)
    
    # 각 구독 항목의 번호를 계산하여 추가
    for index, subscription in enumerate(subscriptions, start=1):
        subscription.number = len(subscriptions_list) - (subscriptions.start_index() + index - 1) + 1
    
    return render(request, 'accounts/subscription_management.html', {'subscriptions': subscriptions})

def unsubscribed_players(request):
    # 현재 로그인한 사용자가 구독한 선수들의 목록을 가져옵니다.
    subscribed_players = Subscription.objects.filter(subscriber=request.user).values_list('subscribed_to_player', flat=True)

    # 구독하지 않은 선수들의 목록을 가져옵니다.
    unsubscribed_players = Player.objects.exclude(id__in=subscribed_players)

    context = {
        'players' : unsubscribed_players
    }

    return render(request, 'payments/pay_home.html', context)

@require_POST
def cancel_subscription(request):
    subscription_id = request.POST.get('subscription_id')
    try:
        subscription = Subscription.objects.get(id=subscription_id, subscriber=request.user)
        payment = SubscriptionPayment.objects.filter(
            user=request.user, 
            player=subscription.subscribed_to_player, 
            plan=subscription.plan
        ).order_by('-created_at').first()
        
        if not payment:
            return JsonResponse({'status': 'error', 'message': '해당 구독에 대한 결제 정보를 찾을 수 없습니다.'})
        

        response = cancel_scheduled_payment(payment.customer_uid, payment.next_merchant_uid)

        print(f"Cancel scheduled payment response: {response}")

        
        if response.get('schedule_status') == 'revoked':
            # 취소 성공
            return JsonResponse({'status': 'success', 'message': '구독이 성공적으로 취소되었습니다.'})
        else:
            # 취소 실패
            fail_reason = response.get('fail_reason', '취소에 실패했습니다.')
            return JsonResponse({'status': 'error', 'message': fail_reason})
    except Subscription.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '해당 구독을 찾을 수 없습니다.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})