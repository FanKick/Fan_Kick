from django.urls import path
from . import views

app_name = "chattings"

urlpatterns = [
    path('', views.redirect_to_dm, name='redirect_to_dm'),
]
