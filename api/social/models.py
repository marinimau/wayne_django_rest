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
from django.utils.translation import gettext_lazy as _


class SocialAccount(models.Model):
    # ------------------------------------------------------------------------------------------------------------------
    #
    # SocialAccount
    #
    # This model store the social media contact of the users.
    #
    # Each social account has the following attributes:
    #
    # - id: index (read_only)
    # - user: User (read_only)
    # - type: {telephone, email, url, username}
    # - required: bool
    # - creation_timestamp: timestamp
    # ------------------------------------------------------------------------------------------------------------------

    class ContactType(models.TextChoices):
        URI = 'URI', _('URI')
        USERNAME = 'USERNAME', _('USERNAME')
        EMAIL = 'EMAIL', _('EMAIL')
        PHONE = 'PHONE', _('PHONE')

    class Meta:
        unique_together = ['platform', 'value']

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_account')
    type = models.CharField(null=False, max_length=8, choices=ContactType.choices, default=ContactType.URI)
    required = models.BooleanField(null=False, default=False)
    creation_timestamp = models.DateTimeField(blank=False, default=now)

    def __str__(self):
        return self.user.username + str(self.id)


class SocialAccountUsername(SocialAccount):
    # ------------------------------------------------------------------------------------------------------------------
    #
    # SocialAccountUsername (subclass of SocialAccount)
    #
    # This model store the social media based on username.
    #
    # Each social username account has the following attributes:
    # - type: {username}
    # - platform: dict, the social username platform
    # - value: string (must be of the given type)
    # ------------------------------------------------------------------------------------------------------------------

    class UsernamePlatforms(models.TextChoices):
        WAYNE = 'WAYNE', _('WAYNE')
        FACEBOOK = 'FACEBOOK', _('FACEBOOK')
        INSTAGRAM = 'INSTAGRAM', _('INSTAGRAM')
        LINKEDIN = 'LINKEDIN', _('LINKEDIN')
        TELEGRAM = 'TELEGRAM', _('TELEGRAM')
        PAYPALL = 'PAYPAL', _('PAYPAL')
        GITHUB = 'GITHUB', _('GITHUB')

    platform = models.CharField(null=False, max_length=40, choices=UsernamePlatforms.choices,
                                default=UsernamePlatforms.WAYNE)
    type = models.CharField(null=False, max_length=8, default=SocialAccount.ContactType.URI)
    value = models.CharField(null=False, max_length=20)


class SocialAccountEmail(SocialAccount):
    # ------------------------------------------------------------------------------------------------------------------
    #
    # SocialAccountEmail (subclass of SocialAccount)
    #
    # This model store the email account.
    #
    # Each email account has the following attributes:
    # - type: {username}
    # - provider: dict, the email provider
    # - value: string (must be of the given type)
    # ------------------------------------------------------------------------------------------------------------------

    class EmailProviders(models.TextChoices):
        OTHER = 'OTHER', _('OTHER')
        GMAIL = 'GMAIL', _('GMAIL')
        MICROSOFT = 'MICROSOFT', _('MICROSOFT')
        EXCHANGE = 'EXCHANGE', _('EXCHANGE')
        YAHOO = 'YAHOO', _('YAHOO')
        LIBERO = 'LIBERO', _('LIBERO')
        TISCALI = 'TISCALI', _('TISCALI')

    provider = models.CharField(null=False, max_length=40, choices=EmailProviders.choices)
    type = models.CharField(null=False, max_length=8, default=SocialAccount.ContactType.EMAIL)
    value = models.EmailField(null=False)
