from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Subscription

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