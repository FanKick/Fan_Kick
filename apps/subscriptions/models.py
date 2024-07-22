from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.accounts.models import CustomUser, Player

class SubscriptionPlan(models.Model):
    sub_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.PositiveIntegerField(help_text='구독기간')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()  # 현재 시간으로 업데이트
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sub_name

class Subscription(models.Model):
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_to_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='subscribers')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscription_plan')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration)
        super().save(*args, **kwargs)
    
    @classmethod
    def has_active_subscription(cls, subscriber, player):
        return cls.objects.filter(
            subscriber=subscriber, 
            subscribed_to_player=player, 
            status=True,
            end_date__gte=timezone.now()
        ).exists()


    def __str__(self):
        return f'Subscription #{self.id} - {self.subscriber.username} to {self.subscribed_to_player.player_name}'