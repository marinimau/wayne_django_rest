from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Profile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M', _('M')
        FEMALE = 'F', _('F')
        OTHER = 'O', _('O')
        UNSPECIFIED = 'U', _('U')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    cellular = models.CharField(null=True, max_length=40, blank=True)
    gender = models.CharField(null=False, max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIED)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ResetPasswordToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reset_password_token', primary_key=True)
    email = models.CharField(max_length=50, blank=False)
    token = models.CharField(max_length=50, blank=False)
    user_agent = models.CharField(max_length=100, blank=True)
    ip = models.CharField(max_length=15, blank=True)
    creation_timestamp = models.DateTimeField(blank=False, default=now)

    def __str__(self):
        return self.token
