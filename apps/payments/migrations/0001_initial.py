# Generated by Django 5.0.6 on 2024-07-29 11:29


import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('subscriptions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', models.JSONField(default=dict, editable=False, verbose_name='포트원 결제내역')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.PositiveIntegerField(editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ready', '미결제'), ('paid', '결제완료'), ('cancelled', '결제취소'), ('failed', '결제실패')], db_index=True, default='ready', max_length=9)),
                ('is_paid', models.BooleanField(db_index=True, default=False, verbose_name='결제성공 여부')),
                ('customer_uid', models.CharField(editable=False, max_length=100)),
                ('next_merchant_uid', models.CharField(blank=True, max_length=40, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscriptionplan')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.player')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
