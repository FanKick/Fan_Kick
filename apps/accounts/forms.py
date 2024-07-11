from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm): # 'username', 'password1', 'password2'는 UserCreationForm 기본 제공 
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com', 'style': 'color: grey;'}))
    phone_num = forms.CharField(max_length=15, widget=forms.EmailInput(attrs={'placeholder': '- 제외한 번호 ', 'style': 'color: grey;'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_num', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_num = self.cleaned_data['phone_num']
        user.is_active = False  # 이메일 인증 전까지 비활성화
        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailForm(forms.Form):
    email = forms.EmailField(label='이메일', max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email
