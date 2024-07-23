from celery import shared_task
from django.utils import timezone
from .models import Subscription

@shared_task(name='update-subscription-status-every-day')
def update_subscription_status():
       today = timezone.now().date()
       subscriptions = Subscription.objects.filter(end_date__lt=today, status=True)
       for subscription in subscriptions:
           subscription.status = False
           subscription.save()

@shared_task(name='test_task')
def test_task():
       print("Test task executed successfully!")
       return "Test task executed successfully!"