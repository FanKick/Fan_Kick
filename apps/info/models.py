from django.utils.text import slugify
from django.db import models
from apps.accounts.models import Team

class TeamInfo(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='team_info')
    info_team_name = models.CharField(max_length=255, unique=True, blank=True)
    team_club_picture = models.ImageField(upload_to='team_club_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, args, **kwargs):
        if not self.info_team_name:
            self.info_team_name = slugify(self.team.team_name)
        super().save(args, **kwargs)

    def str(self):
        return self.team.team_name
