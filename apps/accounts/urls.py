from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/step1/', views.signup_step1, name='signup_step1'),
    path('signup/email_check/', views.email_check, name='email_check'), 
    path('signup/step2/', views.signup_step2, name='signup_step2'),
    path('signup/step3/', views.signup_step3, name='signup_step3'),
    path('signup/done/', views.signup_done, name='signup_done'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update_user_info/', views.update_user_info, name='update_user_info'),
    path('delete_account/', views.delete_account, name='delete_account'),

]
