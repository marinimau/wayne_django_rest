from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class SocialWall(models.Model):
    # ------------------------------------------------------------------------------------------------------------------
    #
    # SocialWall
    #
    # This model contains all social labels of a given user
    #
    # ------------------------------------------------------------------------------------------------------------------
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_wall', primary_key=True)


class SocialLabel(models.Model):
    # ------------------------------------------------------------------------------------------------------------------
    #
    # Social
    #
    # This model is used to store a label: label provides a group for social account items. There are also a 'system'
    # label: this label is created by default and it isn't editable (except for privacy field).
    #
    # Each label items has the following attributes:
    # - id: index (read_only)
    # - user: User (read_only)
    # - privacy: {public, friends, strict, private}
    # - title: string
    # - system: bool
    # - creation_timestamp: timestamp
    # ------------------------------------------------------------------------------------------------------------------

    class LabelPrivacyConfig(models.TextChoices):
        PRIVATE = 'PRIVATE', _('PRIVATE')
        STRICT = 'STRICT', _('STRICT')
        FRIENDS = 'FRIENDS', _('FRIENDS')
        PUBLIC = 'PUBLIC', _('PUBLIC')
        PARENT = 'PARENT', _('PARENT')

    class Meta:
        unique_together = (('wall', 'title'),)

    id = models.AutoField(primary_key=True)
    wall = models.ForeignKey(SocialWall, on_delete=models.CASCADE)
    privacy = models.CharField(null=False, max_length=10, choices=LabelPrivacyConfig.choices,
                               default=LabelPrivacyConfig.PUBLIC)
    title = models.CharField(null=False, max_length=20)
    required = models.BooleanField(null=False, default=False)
    creation_timestamp = models.DateTimeField(null=False, default=now)

    def __str__(self):
        return self.title


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
    # - privacy: {public, friends, strict, private, parent} if parent, the privacy is set at the value of the label
    # - type: {telephone, email, url, username}
    # - platform: dict, the social platform
    # - value: string (must be of the given type)
    # - label: Label (oneToOne) the label that contains the SocialAccount item
    # - required: bool
    # - creation_timestamp: timestamp
    # ------------------------------------------------------------------------------------------------------------------

    class AccountPrivacyConfig(models.TextChoices):
        PRIVATE = 'PRIVATE', _('PRIVATE')
        STRICT = 'STRICT', _('STRICT')
        FRIENDS = 'FRIENDS', _('FRIENDS')
        PUBLIC = 'PUBLIC', _('PUBLIC')
        PARENT = 'PARENT', _('PARENT')

    class ContactType(models.TextChoices):
        URI = 'URI', _('URI')
        USERNAME = 'USERNAME', _('USERNAME')
        EMAIL = 'EMAIL', _('EMAIL')
        PHONE = 'PHONE', _('PHONE')

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_account')
    privacy = models.CharField(null=False, max_length=10, choices=AccountPrivacyConfig.choices,
                               default=AccountPrivacyConfig.PARENT)
    type = models.CharField(null=False, max_length=8, choices=ContactType.choices, default=ContactType.URI)
    platform = models.CharField(null=False, max_length=30, blank=False, default='no-implementation')
    value = models.CharField(null=False, max_length=100, blank=False, default='no-implementation')
    label = models.OneToOneField(SocialLabel, on_delete=models.CASCADE, related_name='label')
    required = models.BooleanField(null=False, default=False)
    creation_timestamp = models.DateTimeField(blank=False, default=now)

    def __str__(self):
        return self.user.username + str(self.id)