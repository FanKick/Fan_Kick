from django.urls import path
from . import views

app_name = "contents"

urlpatterns = [
    path('team/<int:team_id>/player_post_list/', views.PlayerPostListView.as_view(), name='player_post_list'),
    path('team/<int:team_id>/user_post_list/', views.UserPostListView.as_view(), name='user_post_list'),
    path('post_detail/<int:post_id>/', views.post_detail_json, name='post_detail_json'),  # JSON 응답을 위한 URL 패턴 추가
    path('create_post/player/', views.create_post_player, name='create_post_player'),
    path('create_post/user/', views.create_post_user, name='create_post_user'),
    path('team/<int:team_id>/join/', views.join_team, name='join_team'),
    path('post_detail/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),  # add_comment 경로 추가
    path('post_detail/<int:post_id>/add_like/', views.add_like, name='add_like'),  # add_like 경로 추가
    path('comment/<int:comment_id>/add_like/', views.add_like, name='add_like_comment'),
]