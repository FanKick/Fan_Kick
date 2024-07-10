from django import forms
from .models import Team, CustomUser, Player

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
