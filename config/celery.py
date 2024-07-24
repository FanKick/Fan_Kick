from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab    # 일정 스케줄러

# Django의 settings 모듈을 Celery의 기본 설정으로 사용
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('FanKick')

# 여기서 문자열을 사용하는 것은 작업자가 자식 프로세스에서 설정 객체를 직렬화하지 않도록 하기 위함입니다.
# -namespace='CELERY'는 모든 Celery 관련 구성 키가 'CELERY_' 접두사로 시작해야 함을 의미합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django의 모든 등록된 task 모듈을 로드합니다.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

# 정기 작업 스케줄 정의
app.conf.beat_schedule = {
       'update-subscription-status-every-day': {
           'task': 'apps.subscriptions.tasks.update_subscription_status',
           'schedule': crontab(hour=0, minute=0),  # 매일 자정에 실행
       },
   }