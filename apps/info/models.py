from django.utils.text import slugify
from django.db import models
from apps.accounts.models import Team

from django.db import models
from django.conf import settings
from apps.accounts.models import Player

class PlayerInfo(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='info')
    info_player_name = models.CharField(max_length=100, unique=True, blank=True)
    player_picture = models.ImageField(upload_to='player_pictures/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.info_player_name:
            self.info_player_name = slugify(self.player.player_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.player.player_name



class TeamInfo(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='team_info')
    info_team_name = models.CharField(max_length=255, unique=True, blank=True)
    team_club_picture = models.ImageField(upload_to='team_club_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.info_team_name:
            self.info_team_name = slugify(self.team.team_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team.team_name
