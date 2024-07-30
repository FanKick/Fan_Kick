from django.urls import path
from . import views

app_name = "subscriptions"


urlpatterns = [
    path('subscription_manage/', views.subscription_management, name='subscription_management'),
    path('unsubscribed_players/', views.unsubscribed_players, name='unsubscribed_players'),
    path('cancel_subscription/', views.cancel_subscription, name='cancel_subscription'),
]