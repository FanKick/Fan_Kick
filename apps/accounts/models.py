from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser, Group
import os
import uuid
from django.utils.deconstruct import deconstructible


@deconstructible            # profile 사진 수정 시, media/profiles에 UUID로 파일명 변경 후 저장
class PathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # 파일 이름을 UUID로 변경
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)

class CustomUser(AbstractUser):
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # 고유한 related_name 설정
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='Groups this user belongs to.',
        related_name="customuser_groups",  # 고유한 related_name 설정
    )

    # (('value', 'display'))
    USER_ROLES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('player', 'Player'),
        ('team', 'Team'),
    ]

    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True) # 기본 제공 필드 username으로 닉네임 대체
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    profile = models.ImageField(upload_to=PathAndRename('profiles/'), blank=True, null=True)    # 프로필 사진 저장
    is_player = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    joined_teams = models.ManyToManyField('Team', through='Membership', related_name='members', blank=True)

    def save(self, *args, **kwargs):
        try:
            this = CustomUser.objects.get(id=self.id)     
            if this.profile != self.profile:          # 새로운 프로필 사진 저장 시, 기존 파일 삭제
                this.profile.delete(save=False)
        except CustomUser.DoesNotExist:
            pass
        self.updated_at = timezone.now()  # 현재 시간으로 업데이트
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class Team(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='team')
    team_name = models.CharField(max_length=100)
    team_picture = models.ImageField(upload_to='team_pictures/', blank=True, null=True)
    team_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()  # 현재 시간으로 업데이트
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='player')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    player_name = models.CharField(max_length=100)
    position = models.CharField(max_length=5, choices=POSITION_CHOICES)
    birthday = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    back_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

  
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()  # 현재 시간으로 업데이트
        super().save(*args, **kwargs)

    def str(self):
        return self.player_name
    
class Membership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.team.team_name}"