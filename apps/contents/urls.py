from django.urls import path
from . import views

urlpatterns = [
    path('team/<int:team_id>/player_post_list/', views.PlayerPostListView.as_view(), name='player_post_list'),
    path('team/<int:team_id>/user_post_list/', views.UserPostListView.as_view(), name='user_post_list'),
    path('post_detail/<int:post_id>/', views.post_detail_json, name='post_detail_json'),  # JSON 응답을 위한 URL 패턴 추가
    path('create_post/player/', views.create_post_player, name='create_post_player'),
    path('create_post/user/', views.create_post_user, name='create_post_user'),
    path('join_team/', views.join_team, name='join_team'),
     path('post_detail/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),  # add_comment 경로 추가
]