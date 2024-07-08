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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_name

class Subscription(models.Model):
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_to_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='subscribers')
    plan_id = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscription_plan')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timezone.timedelta(days=self.plan_id.duration)
        super().save(*args, **kwargs)

    def is_active_subscription(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return f'Subscription #{self.id} - {self.subscriber.username} to {self.subscribed_to_player.player_name}'