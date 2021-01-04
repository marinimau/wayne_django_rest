#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from rest_framework import serializers
from contents.messages.get_messages import get_messages
from django.conf import settings
from ..models import Config


messages = get_messages(package=settings.CONTENT_PACKAGES[2])


# ----------------------------------------------------------------------------------------------------------------------
#
# ConfigSerializer
#
# This file contains the ConfigSerializer validation functions to check the user input:
#
#  - validate_country
#  - validate_location
#  - validate_language
#
# ----------------------------------------------------------------------------------------------------------------------

def validate_country(instance, validated_data):
    country = validated_data.get('country', instance.country)
    if country != instance.country:
        # if the request edit language field
        if country in Config.Country:
            instance.country = country
            return
        else:
            error = {'message': messages['invalid_country_error']}
            raise serializers.ValidationError(error)


def validate_language(instance, validated_data):
    language = validated_data.get('language', instance.language)
    if language != instance.language:
        # if the request edit language field
        if language in Config.Language:
            instance.language = language
            return
        else:
            error = {'message': messages['invalid_language_error']}
            raise serializers.ValidationError(error)


def validate_ui_pref(instance, validated_data):
    ui_pref = validated_data.get('ui_pref', instance.ui_pref)
    if ui_pref != instance.ui_pref:
        # if the request edit language field
        if ui_pref in Config.UIMode:
            instance.ui_pref = ui_pref
            return
        else:
            error = {'message': messages['invalid_ui_pref_error']}
            raise serializers.ValidationError(error)
