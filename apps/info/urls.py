from django.urls import path
from . import views as info_views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('team/<str:team_name_search>/', info_views.team_info_by_team_name, name='team_info_by_team_name'),
    path('player/<str:player_name_search>/', info_views.team_info_by_player_name, name='team_info_by_player_name'),
]