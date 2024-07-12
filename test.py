import os
from dotenv import load_dotenv
import django
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

# .env 파일 로드
load_dotenv()

# Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE'))

# Django 초기화
django.setup()

def send_activation_email(user):
    token = default_token_generator.make_token(user)      # 사용자 활성화를 위한 토큰 생성
    uid = urlsafe_base64_encode(force_bytes(user.pk))       # 현재 사용자의 기본키를 바이트 문자열 변환 -> 인코딩
    activation_url = settings.SITE_URL + f'/activate/{uid}/{token}/'
    
    # 토큰과 UID를 로그로 출력
    print(f"Generated token: {token}")
    print(f"Encoded UID: {uid}")
    print(f"Activation URL: {activation_url}")

    html_message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })

    plain_message = strip_tags(html_message)      # HTML 태그 제거

    send_mail(
        'Activate Your Account',
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        ['hyunssu1130@naver.com'],
        html_message=html_message,
        fail_silently=False,
    )
