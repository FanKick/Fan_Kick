from django.urls import path
from . import views

app_name = "subscriptions"


urlpatterns = [
    path('subscription_manage/', views.subscription_management, name='subscription_management'),
]