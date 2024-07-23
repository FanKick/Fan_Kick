from django.contrib import admin
from .models import SubscriptionPlan, Subscription
from django.utils import timezone

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('sub_name', 'price', 'duration', 'created_at', 'updated_at')
    search_fields = ('sub_name',)  # 검색 필드 설정
    list_filter = ('created_at', 'updated_at')  # 필터 설정

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'subscribed_to_player', 'plan_id', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')  # 필터 설정
    search_fields = ('subscriber__username', 'subscribed_to_player__player_name')  # 관련 객체의 필드를 사용하여 검색 설정