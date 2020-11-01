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
from django.utils.translation import gettext_lazy as _


# ----------------------------------------------------------------------------------------------------------------------
# Config
#
# This model is used to store the user preferences for his client.
# The model has the following attributes:
#
# - Country : enum  (store the current country)
# - Language : enum (store the language to use in the client app)
# - UIMode : enum (store the theme to use in the client app)
# ----------------------------------------------------------------------------------------------------------------------

class Config(models.Model):
    class Country(models.TextChoices):
        IT = 'IT', _('Italy')
        US = 'US', _('United States')
        FR = 'FR', _('France')

    class Language(models.TextChoices):
        IT = 'IT', _('Italy')
        EN = 'EN', _('English')

    class UIMode(models.TextChoices):
        L = 'L', _('Light')
        D = 'D', _('Dark')
        A = 'A', _('Auto')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='config', primary_key=True)
    country = models.CharField(null=False, max_length=2, choices=Country.choices, default=Country.IT)
    language = models.CharField(null=False, max_length=2, choices=Language.choices, default=Language.EN)
    ui_pref = models.CharField(null=False, max_length=1, choices=UIMode.choices, default=UIMode.A)
