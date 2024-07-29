from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from apps.accounts.models import Team

class TeamInfo(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='team_info')
    team_name = models.CharField(max_length=255, default='default_team_name')
    team_name_search = models.CharField(max_length=255, unique=True, blank=True)  # URL에서 사용할 팀 이름
    team_club_picture = models.ImageField(upload_to='team_club_pictures/', null=True, blank=True)
    team_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.team_name_search:
            self.team_name_search = slugify(self.team_name)
            counter = 1
            while TeamInfo.objects.filter(team_name_search=self.team_name_search).exists():
                self.team_name_search = f"{self.team_name_search}-{counter}"
                counter += 1
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name
