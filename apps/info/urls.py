from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    # path('', views.search_view, name='search'),
    # path('team/<slug:info_team_name>/', views.team_detail, name='team_detail'),
    path('player/<slug:info_player_name>/', views.player_detail, name='player_detail'),
]