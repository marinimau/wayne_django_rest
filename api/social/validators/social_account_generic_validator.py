#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 28/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers


# ----------------------------------------------------------------------------------------------------------------------
#   validate_user
# ----------------------------------------------------------------------------------------------------------------------
def validate_user(context):
    request = context.get("request")
    if request and hasattr(request, "user"):
        return request.user
    else:
        error = {'message': 'invalid value for gender'}
        raise serializers.ValidationError(error)

