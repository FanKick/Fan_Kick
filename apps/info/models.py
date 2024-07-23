# 1. Id (pk)
# 2. user_id (fk)
# 3. team_name
# 4. banner - team_club_pictures/
# 5. team_description
# 6. created_at
# 7. updated_at

from django.db import models
from apps.accounts.models import Team

class TeamInfo(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='team_info')
    team_name = models.CharField(max_length=255, default='default_team_name')
    team_club_picture = models.ImageField(upload_to='team_club_pictures/', null=True, blank=True)
    team_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name
