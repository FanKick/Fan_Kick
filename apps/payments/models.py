from django.db import models
from uuid import UUID, uuid4
from django.conf import settings
from iamport import Iamport
import logging
from django.http import Http404
from django.utils.functional import cached_property
from apps.accounts.models import *
from apps.subscriptions.models import SubscriptionPlan, Subscription
from django.utils import timezone
from .services import schedule_payment

logger = logging.getLogger(__name__)


class AbstractPortonePayment(models.Model):
    class StatusChoices(models.TextChoices):
        READY = "ready", "미결제"
        PAID = "paid", "결제완료"
        CANCELLED = "cancelled", "결제취소"
        FAILED = "failed", "결제실패"
    
    meta = models.JSONField("포트원 결제내역", default=dict, editable=False)
    uid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=9, 
        default=StatusChoices.READY,
        choices=StatusChoices.choices,
        db_index=True,
    )

    is_paid = models.BooleanField("결제성공 여부", default=False, db_index=True)
    
    @property
    def merchant_uid(self):
        return self.uid
    
    @cached_property
    def api(self):
        return Iamport(
            imp_key=settings.PORTONE_API_KEY, imp_secret=settings.PORTONE_API_SECRET
        )
    
    # 결제검증
    def portone_check(self, commit=True):

        try:
            self.meta = self.api.find(merchant_uid=self.merchant_uid)
        except (Iamport.ResponseError, Iamport.HttpError) as e:
            logger.error(str(e), exc_info=e)
            raise Http404("포트원에서 결제내역을 찾을 수 없습니다")
        
        self.status = self.meta['status']
        self.is_paid = self.api.is_paid(self.amount, response=self.meta)

        #TODO : status = PAID인데 is_paid가 False인 경우
        
        if commit:
            self.save()

    class Meta:
        abstract = True


class SubscriptionPayment(AbstractPortonePayment):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscription_payments')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    customer_uid = models.CharField(max_length=100, editable=False)
    next_merchant_uid = models.CharField(max_length=40, blank=True, null=True)


    @classmethod
    def create_by_payment(cls, player, subscriber, plan_name):
        plan = SubscriptionPlan.objects.get(sub_name=plan_name)
        customer_uid = f"cust_{subscriber.id}"
        payment = cls.objects.create(
            name=f"{player.player_name} 구독권",
            amount=plan.price,
            player=player,
            user = subscriber,
            plan=plan,
            customer_uid=customer_uid,
        )

        return payment

    
    def schedule_next_payment(self, retry=False):
        # 정기결제 결제실패할 시, 하루 뒤 재시도
        if retry:
            schedule_at = float((timezone.now() + timezone.timedelta(days=1)).timestamp())
        else:
            # schedule_at = float((timezone.now() + timezone.timedelta(minutes=2)).timestamp())
            schedule_at = float((timezone.now() + timezone.timedelta(days=self.plan.duration)).timestamp())

        self.next_merchant_uid = uuid.uuid4()
        self.save()

        schedule_payment(
            customer_uid=self.customer_uid,
            merchant_uid=str(self.next_merchant_uid),
            amount=self.amount,
            schedule_at=schedule_at,
            name=f"{self.player.player_name} 구독권",
        )

  
    def create_subscription_if_paid(self):
        if self.is_paid:
            Subscription.objects.create(
                subscriber=self.user,
                subscribed_to_player=self.player,
                plan=self.plan,
                start_date=timezone.now().date(),
            )

            # 결제 성공시에만 다음 결제 예약
            self.schedule_next_payment()

    def save_schedule_payment(self):
        try:

            meta = self.api.find(merchant_uid=self.next_merchant_uid)

            # 예약결제건 결제내역 저장
            payment = SubscriptionPayment.objects.create(
                uid=self.next_merchant_uid,
                player=self.player,
                plan=self.plan,
                customer_uid=self.customer_uid,
                amount=self.amount,
                status = self.meta['status'],
                name=self.name,
                meta=meta,
                user=self.user,
            )

            payment.portone_check(commit=True)

            # 결제 성공시, 구독권 연장
            if self.is_paid:

                subscription = Subscription.objects.filter(
                subscriber=self.user,
                subscribed_to_player=self.player,
                plan=self.plan,
                status=True
                ).first()

                subscription.end_date += timezone.timedelta(days=self.plan.duration)
                subscription.save()


            payment.schedule_next_payment()

        except Exception as e:
            print(f"Error in save_schedule_payment: {str(e)}")
            raise