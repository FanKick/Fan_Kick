# Generated by Django 5.0.6 on 2024-07-29 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_community_communitymembership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitymembership',
            name='community',
        ),
        migrations.RemoveField(
            model_name='communitymembership',
            name='user',
        ),
        migrations.DeleteModel(
            name='Community',
        ),
        migrations.DeleteModel(
            name='CommunityMembership',
        ),
    ]
