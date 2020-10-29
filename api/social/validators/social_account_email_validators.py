#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 28/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers
from api.social.models import SocialAccountEmail
from django.core.validators import validate_email


# ----------------------------------------------------------------------------------------------------------------------
#   validate email account
# ----------------------------------------------------------------------------------------------------------------------
def validate_email_account_creation(validated_data):
    platform = validated_data.pop('platform', None)
    value = validated_data.pop('value', None)
    validate_email_account(platform, value)
    return platform, value


# ----------------------------------------------------------------------------------------------------------------------
#   validate email account
# ----------------------------------------------------------------------------------------------------------------------
def validate_email_account(platform, value):
    validate_platform(platform)
    validate_value(value)
    if SocialAccountEmail.objects.filter(value=value).count() > 0:
        error = {'message': 'this account already exists'}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   validate provider
# ----------------------------------------------------------------------------------------------------------------------
def validate_platform(platform):
    if platform not in SocialAccountEmail.EmailProviders:
        error = {'message': 'invalid email provider'}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   validate value
# ----------------------------------------------------------------------------------------------------------------------
def validate_value(value):
    try:
        validate_email(value)
    except Exception:
        error = {'message': 'invalid email'}
        raise serializers.ValidationError(error)


# ----------------------------------------------------------------------------------------------------------------------
#   update value
# ----------------------------------------------------------------------------------------------------------------------
def update_value(instance, value):
    if value != instance.value:
        validate_email_account(instance.platform, value)
        instance.value = str.lower(value)
