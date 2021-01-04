#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.utils import timezone
from rest_framework import serializers
from contents.messages.get_messages import get_messages
from django.conf import settings
from ..models import ResetPasswordToken


messages = get_messages(package=settings.CONTENT_PACKAGES[1])


# ----------------------------------------------------------------------------------------------------------------------
# change password validators
# ----------------------------------------------------------------------------------------------------------------------
def check_if_already_exists_and_delete_token(user):
    ResetPasswordToken.objects.filter(user=user).delete()
    return


def get_token_by_user(user):
    if ResetPasswordToken.objects.filter(user=user).exists():
        return ResetPasswordToken.objects.get(user=user)
    else:
        error = {'message': messages['no_token_error']}
        raise serializers.ValidationError(error)


def compare_and_validate_tokens(token_obj, validated_data):
    token_get = validated_data.get('token', None)
    if token_get is not None and token_obj.token == token_get:
        if token_obj.creation_timestamp is not None and (timezone.now() - token_obj.creation_timestamp).days <= 1:
            return True
        else:
            error = {'message': messages['token_expired_error']}
            raise serializers.ValidationError(error)
    else:
        error = {'message': messages['invalid_token_error']}
        raise serializers.ValidationError(error)
