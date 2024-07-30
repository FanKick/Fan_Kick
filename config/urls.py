from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
from apps.info import views as info_views 

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('contents/', include('apps.contents.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('chattings/', include('apps.chattings.urls')),
    path('player/noone/', TemplateView.as_view(template_name="info/noone_info_detail.html"), name='noone_info_detail'),
    path('team/<str:info_team_name>/', info_views.team_detail, name='team_detail'),
    path('player/<str:info_player_name>/', info_views.player_detail, name='player_detail'),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('payments/', include('apps.payments.urls')),
    path('search/', include('apps.search.urls', namespace='search')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
