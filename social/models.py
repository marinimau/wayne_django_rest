from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class SocialLabel(models.Model):

    def __str__(self):
        pass


class SocialAccount(models.Model):

    # ------------------------------------------------------------------------------------------------------------------
    #
    # SocialAccount
    #
    # This class store the social media contact of the users.
    #
    # Each social account has the following attributes:
    #
    # - id: index (read_only)
    # - user: User (read_only)
    # - privacy: {public, friends, strict, private, parent}
    # - type: {telephone, email, url, username}
    # - platform: dict, the social platform
    # - label: Label (oneToOne) the label that contains the SocialAccount item
    # - creation_timestamp: timestamp
    # ------------------------------------------------------------------------------------------------------------------

    class PrivacyConfig(models.TextChoices):
        PRIVATE = 'PRIVATE', _('PRIVATE')
        STRICT = 'STRICT', _('STRICT')
        FRIENDS = 'FRIENDS', _('FRIENDS')
        PUBLIC = 'PUBLIC', _('PUBLIC')
        PARENT = 'PARENT', _('PARENT')

    class ContactType(models.TextChoices):
        URI = 'URI', _('URI')
        USERNAME = 'USERNAME', _('USERNAME')
        PHONE = 'PHONE', _('PHONE')

    id = models.Index()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    privacy = models.CharField(null=False, max_length=10, choices=PrivacyConfig.choices, default=PrivacyConfig.PARENT)
    type = models.CharField(null=False, max_length=10, choices=ContactType.choices, default=ContactType.URI)
    creation_timestamp = models.DateTimeField(blank=False, default=now)

    def __str__(self):
        return self.user.username + str(self.id)





