# apps/info/urls.py

from django.urls import path
from . import views

app_name = "info"

urlpatterns = [
    path('<int:pk>/', views.team_info_detail, name='team_info_detail'),
]