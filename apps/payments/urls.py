from django.urls import path
from . import views

app_name ='payments'
urlpatterns = [
    path('payment/<int:pk>/check/', views.payment_check, name='payment_check'),
    path('payment/<int:pk>/', views.payment_detail, name='payment_detail'),

    path('payment/', views.pay_home, name='pay_home'),
    path('payment/<int:pk>/subsctiption_pay/', views.subsctiption_pay, name='subsctiption_pay'),

    # path('subscribe_payment/<int:pk>/', views.subscribe_payment, name='subscribe_payment'),
    # path('get_customer_uid/<int:pk>/', views.get_customer_uid, name='get_customer_uid'),
    # path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('cancel_schedule_payment/<int:pk>/', views.cancel_schedule_payment, name='cancel_schedule_payment'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
]