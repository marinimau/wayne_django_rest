#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


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



