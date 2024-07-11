from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def send_activation_email(user):    # 회원가입 시, 이메일 입력 후 이메일 인증을 위해 전송됨
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activation_url = f"{settings.SITE_URL}{activation_link}"

    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })
    email = EmailMessage('Account Activation', message, to=[user.email])
    email.send()
