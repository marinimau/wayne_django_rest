#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from ..models import Config
from rest_framework import serializers

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
    country = validated_data.get('country', instance.country).upper()
    if country != instance.country:
        # if the request edit language field
        if country in dict(Config.Country.choices):
            instance.country = country
            return
        else:
            error = {'message': 'invalid value for country'}
            raise serializers.ValidationError(error)


def validate_language(instance, validated_data):
    language = validated_data.get('language', instance.language).upper()
    if language != instance.language:
        # if the request edit language field
        if language in dict(Config.Language.choices):
            instance.language = language
            return
        else:
            error = {'message': 'invalid value for language'}
            raise serializers.ValidationError(error)


def validate_ui_pref(instance, validated_data):
    ui_pref = validated_data.get('ui_pref', instance.ui_pref).upper()
    if ui_pref != instance.ui_pref:
        # if the request edit language field
        if ui_pref in dict(Config.UIMode.choices):
            instance.ui_pref = ui_pref
            return
        else:
            error = {'message': 'invalid choice for UI pref'}
            raise serializers.ValidationError(error)