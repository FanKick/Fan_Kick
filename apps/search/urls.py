from django.urls import path
from .views import search_view, player_detail_view, autocomplete

app_name = 'search'

urlpatterns = [
    path('', search_view, name='search'),
    path('autocomplete/', autocomplete, name='autocomplete'),
]
