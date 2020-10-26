#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

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
