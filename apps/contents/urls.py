from django.urls import path
from . import views

urlpatterns = [
    path('player_post_list/', views.PlayerPostListView.as_view(template_name='contents/player_post_list.html'), name='player_post_list'),
    path('user_post_list/', views.UserPostListView.as_view(template_name='contents/user_post_list.html'), name='user_post_list'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(template_name='contents/post_detail.html'), name='post_detail'),
    path('create/', views.create_post, name='create_post'),
]