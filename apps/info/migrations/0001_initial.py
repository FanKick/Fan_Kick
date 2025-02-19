# Generated by Django 5.0.6 on 2024-07-29 11:29


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info_player_name', models.CharField(blank=True, max_length=100, unique=True)),
                ('player_picture', models.ImageField(blank=True, null=True, upload_to='player_pictures/')),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='accounts.player')),
            ],
        ),
        migrations.CreateModel(
            name='TeamInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info_team_name', models.CharField(blank=True, max_length=255, unique=True)),
                ('team_club_picture', models.ImageField(blank=True, null=True, upload_to='team_club_pictures/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team_info', to='accounts.team')),
            ],
        ),
    ]
