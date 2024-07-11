from django.urls import path
from .views import signup, activate
from django.views.generic import TemplateView


app_name = "orders"

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
     path('signup_done/', TemplateView.as_view(), name='signup_done'),
]