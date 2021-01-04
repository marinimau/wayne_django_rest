#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 28/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

import re

from rest_framework import serializers
from contents.messages.get_messages import get_messages
from django.conf import settings
from api.social.models import SocialAccountUsername


messages = get_messages(package=settings.CONTENT_PACKAGES[3])


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
        error = {'message': messages['account_already_exists_error']}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   validate platform
# ----------------------------------------------------------------------------------------------------------------------
def validate_platform(platform):
    if not (platform in SocialAccountUsername.UsernamePlatforms):
        error = {'message': messages['invalid_username_provider_error']}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   validate value
# ----------------------------------------------------------------------------------------------------------------------
def validate_value(value):
    if re.match("^[a-zA-Z0-9_.-]+$", value) is None:
        error = {'message': messages['invalid_username_error']}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   update value
# ----------------------------------------------------------------------------------------------------------------------
def update_value(instance, value):
    if value != instance.value:
        validate_user_account(instance.platform, value)
        instance.value = str.lower(value)
