from django import forms
from .models import Team, CustomUser, Player
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(is_team=True)

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(is_player=True)


from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import re

class EmailForm(forms.Form):          # email 입력 폼
    email = forms.EmailField(
        max_length=254, 
        label='이메일',
        #help_text='Enter a valid email address.',
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'form-control'})
    )

class PasswordForm(UserCreationForm):     # PW 입력 폼
    password1 = forms.CharField(
        label='새로운 비밀번호',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '새로운 비밀번호', 'class': 'form-control'}),
        #help_text=_("Your password must be 8-32 characters long, and include at least one letter, one number, and one special character."),
    )
    password2 = forms.CharField(
        label='새로운 비밀번호 확인',
        widget=forms.PasswordInput(attrs={'placeholder': '새로운 비밀번호 확인', 'class': 'form-control'}),
        strip=False,
        #help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = CustomUser
        fields = ('password1', 'password2')

    def clean_password1(self):      # 조건 부합 유효성 검사
        password1 = self.cleaned_data.get('password1')

        # 최소 길이 8자, 최대 길이 32자
        if len(password1) < 8 or len(password1) > 32:
            raise forms.ValidationError("비밀번호는 8자 이상 32자 이하이어야 합니다.")

        # 영문, 숫자, 특수문자 각각 1글자 이상 포함 여부 확인
        if not re.search(r'[a-zA-Z]', password1):
            raise forms.ValidationError("비밀번호에는 최소 한 글자의 영문자가 포함되어야 합니다.")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("비밀번호에는 최소 한 글자의 숫자가 포함되어야 합니다.")
        if not re.search(r'[~!@#$%^&*()_+{}":?><|,./;\'\[\]\\]', password1):
            raise forms.ValidationError("비밀번호에는 최소 한 글자의 특수문자가 포함되어야 합니다.")

        return password1

        def clean_password2(self):      # 1, 2 비밀번호 일치여부 확인
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return password2

class UserInfoForm(forms.ModelForm):      # 닉네임 및 휴대폰 번호 입력 폼
    phone_num = forms.CharField(
        max_length=15, 
        #help_text='Enter a valid phone number without dashes.',
        widget=forms.TextInput(attrs={'placeholder': '01000000000','class': 'form-control'})
    )
    
    username = forms.CharField(
        max_length=32,
        #help_text='닉네임은 1~32자 길이이어야 하며, 숫자와 특수문자를 포함해야 합니다.',
        widget=forms.TextInput(attrs={'placeholder': 'Members_wh0k0a', 'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_num')

    def clean_username(self):
        username = self.cleaned_data['username']

        # 닉네임 길이 확인
        if len(username) < 1 or len(username) > 32:
            raise forms.ValidationError('닉네임은 1자 이상 32자 이하이어야 합니다.')

        # 숫자와 특수문자 포함 여부 확인
        if not re.search(r'\d', username) or not re.search(r'[~!@#$%^&*()_+{}":?><|,./;\'\[\]\\]', username):
            raise forms.ValidationError('닉네임은 숫자와 특수문자를 포함해야 합니다.')

        # 기존에 존재하는 닉네임인지 확인
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')

        return username
    
    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']

        # 전화번호 길이 확인
        if len(phone_num) < 10 or len(phone_num) > 15:
            raise forms.ValidationError('전화번호는 10자에서 15자 사이의 숫자로 구성되어야 합니다.')

        # 전화번호 숫자 여부 확인
        if not phone_num.isdigit():
            raise forms.ValidationError('전화번호는 숫자만 포함할 수 있습니다.')

        return phone_num

class LoginForm(forms.Form):
    email = forms.EmailField(label='이메일', max_length=200, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com','class': 'form-control'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'placeholder': 'PW', 'class': 'form-control'}))


# mypage -  회원정보 수정
from django import forms
from .models import CustomUser
import re

class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username']

        # 닉네임 길이 확인
        if len(username) < 1 or len(username) > 32:
            raise forms.ValidationError('닉네임은 1자 이상 32자 이하이어야 합니다.')

        # 숫자와 특수문자 포함 여부 확인
        if not re.search(r'\d', username) or not re.search(r'[~!@#$%^&*()_+{}":?><|,./;\'\[\]\\]', username):
            raise forms.ValidationError('닉네임은 숫자와 특수문자를 포함해야 합니다.')

        # 기존에 존재하는 닉네임인지 확인
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')

        return username

class UpdatePhoneNumForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone_num']

    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']

        # 전화번호 길이 확인
        if len(phone_num) < 10 or len(phone_num) > 15:
            raise forms.ValidationError('전화번호는 10자에서 15자 사이의 숫자로 구성되어야 합니다.')

        # 전화번호 숫자 여부 확인
        if not phone_num.isdigit():
            raise forms.ValidationError('전화번호는 숫자만 포함할 수 있습니다.')

        return phone_num

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile']

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')

        if profile:
            # 파일 크기 제한 (예: 2MB)
            max_size = 2 * 1024 * 1024
            if profile.size > max_size:
                raise forms.ValidationError("프로필 사진의 크기는 2MB 이하이어야 합니다.")

            # 파일 형식 제한
            valid_mime_types = ['image/jpeg', 'image/png']
            if profile.content_type not in valid_mime_types:
                raise forms.ValidationError("JPEG 또는 PNG 형식의 이미지만 업로드할 수 있습니다.")

        return profile

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='새로운 비밀번호',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '새로운 비밀번호', 'class': 'form-control'}),
        required=True
    )
    password2 = forms.CharField(
        label='새로운 비밀번호 확인',
        widget=forms.PasswordInput(attrs={'placeholder': '새로운 비밀번호 확인', 'class': 'form-control'}),
        required=True
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # 최소 길이 8자, 최대 길이 32자
        if len(password1) < 8 or len(password1) > 32:
            raise forms.ValidationError("비밀번호는 8자 이상 32자 이하이어야 합니다.")

        # 영문, 숫자, 특수문자 각각 1글자 이상 포함 여부 확인
        if not re.search(r'[a-zA-Z]', password1):
            raise forms.ValidationError("비밀번호에는 최소 한 글자의 영문자가 포함되어야 합니다.")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("비밀번호에는 최소 한 글자의 숫자가 포함되어야 합니다.")
        if not re.search(r'[~!@#$%^&*()_+{}":?><|,./;\'\[\]\\]', password1):
            raise forms.ValidationError("비밀번호에는 최소 한 글자의 특수문자가 포함되어야 합니다.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2