from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class ResetPasswordToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reset_password_token', primary_key=True)
    email = models.CharField(max_length=50, blank=False)
    token = models.CharField(max_length=50, blank=False)
    user_agent = models.CharField(max_length=100, blank=True)
    ip = models.CharField(max_length=15, blank=True)
    creation_timestamp = models.DateTimeField(blank=False, default=now)

    def __str__(self):
        return self.token
