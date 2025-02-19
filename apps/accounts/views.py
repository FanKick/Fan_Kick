from django.shortcuts import render, redirect
from .models import CustomUser
from .utils import send_activation_email
from .forms import EmailForm, PasswordForm, UserInfoForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.contrib import messages
from .tokens import account_activation_token
import pdb

User = get_user_model()

def signup_step1(request):      # email 입력받기
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():       # 기존 유저인지 확인
                form.add_error('email', 'Email is already in use.')
            else:
                request.session['signup_email'] = email
                return redirect('accounts:email_check')  # 이메일 확인 후 안내 페이지로 리디렉션
    else:
        form = EmailForm()
    return render(request, 'accounts/signup_step1.html', {'form': form})

def email_check(request):       # 이메일 기존 유저인지 아닌지 확인
    if 'signup_email' not in request.session:
        return redirect('accounts:signup_step1')

    email = request.session['signup_email']
    return render(request, 'accounts/email_check.html', {'email': email})

def signup_step2(request):       # PW 입력받기
    if 'signup_email' not in request.session:
        return redirect('accounts:signup_step1')

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            request.session['signup_password'] = form.cleaned_data['password1']
            return redirect('accounts:signup_step3')
        else:
            print(form.errors)
    else:
        form = PasswordForm()
    return render(request, 'accounts/signup_step2.html', {'form': form})

def signup_step3(request):      # 닉네임 및 휴대폰 번호 입력받기
    if 'signup_email' not in request.session or 'signup_password' not in request.session:
        return redirect('accounts:signup_step1')

    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone_num = form.cleaned_data['phone_num']
            email = request.session['signup_email']
            password = request.session['signup_password']
            user = CustomUser.objects.create_user(            # DB 값 생성 - new User
                username=username, 
                email=email, 
                password=password,
                phone_num=phone_num,
                is_active=False  # 이메일 인증 전까지 비활성화
            )
            send_activation_email(user)
            return redirect('accounts:signup_done')
    else:
        form = UserInfoForm()
    return render(request, 'accounts/signup_step3.html', {'form': form})

def signup_done(request):         # 회원가입 완료
    return render(request, 'accounts/signup_done.html')


def activate(request, uidb64, token):         # 이메일 인증 후 회원 활성화 by token 값 이용
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        print(f"Decoded UID: {uid}")
        print(f"User found: {user}")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        print(f"Error: {e}")
        user = None

    if user is not None:
        print(f"Token: {token}")
        if account_activation_token.check_token(user, token):
            print("Token is valid.")
            user.is_active = True
            user.save()
            messages.success(request, '인증이 성공했습니다. 이제 로그인이 가능합니다.')
            return redirect('accounts:login')
        else:
            print("Token is invalid.")
    else:
        print("User is None.")

    if user is None:
        messages.error(request, '사용자를 찾을 수 없습니다.')
    else:
        messages.error(request, '인증 링크가 유효하지 않습니다. 다른 이메일로 재시도해보세요.')
    return render(request, 'accounts/activation_invalid.html')



from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import CustomUser

def login_view(request):          # 로그인 구현
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except CustomUser.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect('home')  # 로그인 후 리디렉션할 URL
            else:
                if not CustomUser.objects.filter(email=email).exists():
                    form.add_error('email', '이메일이 존재하지 않습니다.')
                else:
                    form.add_error('password', '비밀번호가 올바르지 않습니다.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')  # 로그아웃 후 리디렉션할 URL


# 마이페이지 - 회원정보수정
from django.contrib.auth.decorators import login_required
from .forms import UpdateUsernameForm, UpdatePhoneNumForm, UpdateProfileForm, UpdatePasswordForm

@login_required
def update_user_info(request):
    if request.method == 'POST':
        username_form = UpdateUsernameForm(instance=request.user)
        phone_num_form = UpdatePhoneNumForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user)
        password_form = UpdatePasswordForm()

        if 'update_username' in request.POST:
            username_form = UpdateUsernameForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, '닉네임이 성공적으로 수정되었습니다.')
                return redirect('accounts:update_user_info')
        elif 'update_phone_num' in request.POST:
            phone_num_form = UpdatePhoneNumForm(request.POST, instance=request.user)
            if phone_num_form.is_valid():
                phone_num_form.save()
                messages.success(request, '전화번호가 성공적으로 수정되었습니다.')
                return redirect('accounts:update_user_info')
        elif 'update_profile' in request.POST:
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, '프로필 사진이 성공적으로 수정되었습니다.')
                return redirect('accounts:update_user_info')
        elif 'update_password' in request.POST:
            password_form = UpdatePasswordForm(request.POST)
            if password_form.is_valid():
                user = request.user
                user.set_password(password_form.cleaned_data['password1'])
                user.save()
                messages.success(request, '비밀번호가 성공적으로 수정되었습니다.')
                return redirect('accounts:update_user_info')
    else:
        username_form = UpdateUsernameForm(instance=request.user)
        phone_num_form = UpdatePhoneNumForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user)
        password_form = UpdatePasswordForm()

    return render(request, 'accounts/update_user_info.html', {
        'username_form': username_form,
        'phone_num_form': phone_num_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })

# 회원탈퇴
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, '회원 탈퇴가 성공적으로 처리되었습니다.')
        return redirect('home')  # 탈퇴 후 리디렉션할 URL
    


# 커뮤니티 관리
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Membership
from apps.contents.models import Post, Comment
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

# 가입 커뮤니티 목록
@login_required
def my_community_view(request):
    memberships_list = Membership.objects.filter(user=request.user).order_by('-date_joined')
    
    # 페이지네이션 설정 (페이지당 5개 항목)
    paginator = Paginator(memberships_list, 5)
    page_number = request.GET.get('page')
    memberships = paginator.get_page(page_number)
    
    # 각 커뮤니티 항목의 번호를 계산하여 추가 (역순으로 번호 매기기)
    for index, membership in enumerate(memberships, start=1):
        membership.number = (len(memberships_list) - (memberships.start_index() + index - 1)) + 1
  
    
    return render(request, 'accounts/my_community.html', {'page_obj': memberships})

# 커뮤니티 탈퇴
@login_required
def leave_community(request, membership_id):
    if request.method == 'POST':
        membership = Membership.objects.filter(id=membership_id, user=request.user).first()
        if membership:
            membership.delete()
            messages.success(request, '커뮤니티에서 탈퇴했습니다.')
        else:
            messages.error(request, '탈퇴할 수 없습니다.')
    return redirect('accounts:my_community')


# 작성한 게시글 내역
@login_required
def my_posts_view(request):         # 작성한 게시글 목록
    posts_list = Post.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(posts_list, 5)  # 5개씩 보여줌
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # 각 게시글 항목의 번호를 계산하여 추가 (역순으로 번호 매기기)
    for index, post in enumerate(posts, start=1):
        post.number = (len(posts_list) - (posts.start_index() + index - 1)) + 1
    
    return render(request, 'accounts/my_posts.html', {'page_obj': posts})


# 게시글 삭제 in 마이페이지
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
    return redirect('accounts:my_posts')  # 게시글 목록 페이지로 리디렉션

@login_required
def my_comments_view(request):      # 작성한 댓글 목록
    comments_list = Comment.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(comments_list, 5)  # 5개씩 보여줌
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    # 각 게시글 항목의 번호를 계산하여 추가 (역순으로 번호 매기기)
    for index, post in enumerate(comments, start=1):
        post.number = (len(comments_list) - (comments.start_index() + index - 1)) + 1
    
    return render(request, 'accounts/my_comments.html', {'page_obj': comments})

# 작성 댓글 삭제
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
    return redirect('accounts:my_comments') 