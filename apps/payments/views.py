import json
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.conf import settings
from .models import *
from apps.accounts.models import *
from apps.subscriptions.models import *
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .services import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

## test 하려고 만든 함수
def pay_home(request):
    players = Player.objects.filter(team__team_name='FC 서울')
    return render(request, 'payments/pay_home.html', 
        {
            'players' : players,
        }
    )


def subsctiption_pay(request,pk):
    player = Player.objects.get(pk=pk)
    subscriber = request.user

    # #TODO: 유효구독 redicrt 디엠창으로
    # if Subscription.has_active_subscription(subscriber, player):
    #     # messages('현재 유효한 구독이 있습니다. 새로운 구독을 결제할 수 없습니다.')

    #     #### fix: 해당 선수와의 디엠창으로 리다이렉트 ####
    #     # return redirect("payments:payment_detail", pk=pk)
    #     raise Http404("현재 유효한 구독이 있습니다")
    
    payment = SubscriptionPayment.create_by_payment(player, subscriber, 'Basic Plan')

    payment_props = {
        'pg': 'kakaopay',
        'merchant_uid': payment.merchant_uid,
        'name': payment.name,
        'amount': payment.amount,
        'customer_uid': payment.customer_uid,
    }

    payment_check_url = reverse("payments:payment_check", args=[payment.pk])
    
    return render(
        request,
        "payments/payment.html",
        {
            "portone_shop_id": settings.PORTONE_SHOP_ID,
            "payment_props": payment_props,
            "payment_check_url": payment_check_url,
        },
    )

def payment_check(request, pk):
    payment = get_object_or_404(SubscriptionPayment, pk=pk)
    
    # 결제검증
    payment.portone_check()

    # 결제 성공시 구독 등록
    payment.create_subscription_if_paid()

    player_info = {
        'player_name': payment.player.player_name,
        'player_profile_image': payment.player.user.profile.url if payment.player.user.profile else None,
    }
    
    response_data = {
        'is_paid': payment.is_paid,
        'player_info': player_info,
    }
    
    if payment.is_paid:
        subscription = Subscription.objects.filter(
            subscriber=payment.user, 
            subscribed_to_player=payment.player, 
            plan=payment.plan
        ).first()
        if subscription:
            response_data['player_info'].update({
                'subscription_start': subscription.start_date.strftime('%Y-%m-%d'),
                'subscription_end': subscription.end_date.strftime('%Y-%m-%d'),
            })
    
    return JsonResponse(response_data)
    # return redirect("payments:payment_detail", pk=pk")


def payment_detail(request, pk):
    payment = get_object_or_404(SubscriptionPayment, pk=pk)
    return render(
        request, 
        "payments/payment_detail.html",
        {
            "payment" : payment,
        }    
    )

def cancel_schedule_payment(request, pk):
    payment = get_object_or_404(SubscriptionPayment, pk=pk)
    
    try:

        recent_payment = SubscriptionPayment.objects.filter(
            customer_uid=payment.customer_uid,
            player_id=payment.player_id
        ).order_by('-created_at').first()


        # 예약된 결제 취소
        response = cancel_scheduled_payment(recent_payment.customer_uid, recent_payment.next_merchant_uid)
        
        ## rediect로 취소내역 보여주는걸로 수정해야함
        return HttpResponse(f"예약된 결제가 취소되었습니다: {response}", status=200)
    
    except Exception as e:
        return HttpResponse(f"예약 취소 실패: {e}", status=400)


@csrf_exempt
@require_POST
def payment_webhook(request):
    try:
        data = json.loads(request.body)
        merchant_uid = data.get('merchant_uid')
        status = data.get('status')

        print(merchant_uid, status)


        # 정기결제 결제완료
        if status == 'paid':
            try:
                payment = SubscriptionPayment.objects.get(uid=merchant_uid)
                pass
                
            except SubscriptionPayment.DoesNotExist:
                payment = SubscriptionPayment.objects.get(next_merchant_uid=merchant_uid)
                payment.save_schedule_payment()
            

        # 정기결제 결제실패
        elif status == 'failed':
            payment = SubscriptionPayment.objects.get(next_merchant_uid=merchant_uid)
            payment.is_paid = False
            payment.save()

            # 재결제 시도
            payment.schedule_next_payment(retry=True)

        # 관리자가 결제취소
        elif status == 'cancelled':
            payment = SubscriptionPayment.objects.get(uid=merchant_uid)

            payment.is_paid = False
            payment.save()

        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        return JsonResponse({'status': 'success'})

    except SubscriptionPayment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Payment not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)