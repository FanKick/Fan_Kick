from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser, Group


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
    nickname = models.CharField(max_length=50, unique=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    profile = models.ImageField(upload_to='media/profiles/', blank=True, null=True)
    is_player = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()  # 현재 시간으로 업데이트
        super().save(*args, **kwargs)

    def str(self):
        return self.username
    
class Team(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='team')
    team_name = models.CharField(max_length=100)
    team_picture = models.ImageField(upload_to='media/team_pictures/', blank=True, null=True)
    team_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()  # 현재 시간으로 업데이트
        super().save(*args, **kwargs)

    def str(self):
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
    updated_at = models.DateTimeField(null=True)

  
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()  # 현재 시간으로 업데이트
        super().save(*args, **kwargs)

    def str(self):
        return self.player_name