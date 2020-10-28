#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 28/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers
from api.social.models import SocialAccountUsername
import re


# ----------------------------------------------------------------------------------------------------------------------
#   validate user account
# ----------------------------------------------------------------------------------------------------------------------
def validate_user_account_creation(validated_data):
    platform = validated_data.pop('platform', None)
    value = validated_data.pop('value', None)
    validate_user_account(platform, value)
    return platform, value


# ----------------------------------------------------------------------------------------------------------------------
#   validate user account
# ----------------------------------------------------------------------------------------------------------------------
def validate_user_account(platform, value):
    validate_platform(platform)
    validate_value(value)
    if SocialAccountUsername.objects.filter(platform=platform, value=value).count() > 0:
        error = {'message': 'this account already exists'}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   validate platform
# ----------------------------------------------------------------------------------------------------------------------
def validate_platform(platform):
    if platform not in SocialAccountUsername.UsernamePlatforms.choices:
        error = {'message': 'invalid username platfom'}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   validate value
# ----------------------------------------------------------------------------------------------------------------------
def validate_value(value):
    if re.match("^[a-zA-Z0-9_.-]+$", value) is None:
        error = {'message': 'invalid username'}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   update value
# ----------------------------------------------------------------------------------------------------------------------
def update_value(instance, value):
    if value != instance.value:
        validate_user_account(instance.platform, value)
        instance.value = str.lower(value)
