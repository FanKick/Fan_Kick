from django.shortcuts import render, redirect
from .forms import SignUpForm
from .utils import send_activation_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 이메일 인증 전까지 비활성화
            user.save()

            # 이메일 인증 링크 전송
            send_activation_email(user)

            # 회원가입 완료 메시지 또는 다른 처리 로직 추가 가능
            return redirect('signup_done')  # 회원가입 완료 페이지로 리다이렉트
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token):   # 사용자가 받은 이메일에서 활성화 링크 클릭 시, 토큰 유효성 검사 후 활성화 결정
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'accounts/activation_invalid.html')
    
class SignUpDoneView(TemplateView):
    template_name = 'accounts/signup_done.html'
