# Generated by Django 3.0.7 on 2020-06-15 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPasswordToken',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='reset_password_token', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('email', models.CharField(max_length=50)),
                ('token', models.CharField(max_length=50)),
                ('user_agent', models.CharField(blank=True, max_length=100)),
                ('ip', models.CharField(blank=True, max_length=15)),
                ('creation_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]