#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 28/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers
from contents.messages.get_messages import get_messages
from django.conf import settings

messages = get_messages(package=settings.CONTENT_PACKAGES[3])


# ----------------------------------------------------------------------------------------------------------------------
#   validate_user
# ----------------------------------------------------------------------------------------------------------------------
def validate_user(context):
    request = context.get("request")
    if request and hasattr(request, "user"):
        return request.user
    else:
        error = {'message': messages['invalid_user_error']}
        raise serializers.ValidationError(error)

