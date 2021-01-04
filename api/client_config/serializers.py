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
from .models import Config
from .validators.config_validators import validate_country, validate_language, validate_ui_pref


messages = get_messages(package=settings.CONTENT_PACKAGES[2])


# ----------------------------------------------------------------------------------------------------------------------
#
# ConfigSerializer
#
# - update fields (country, language, ui_pref)
#
# ----------------------------------------------------------------------------------------------------------------------


class ConfigSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        # validate country
        validate_country(instance, validated_data)
        # validate language
        validate_language(instance, validated_data)
        # validate ui_pref
        validate_ui_pref(instance, validated_data)
        instance.save()
        return instance

    def create(self, validated_data):
        error = {'message': messages['create_not_allowed']}
        raise serializers.ValidationError(error)

    user = serializers.ReadOnlyField(source='user.pk')
    country = serializers.ChoiceField(choices=Config.Country.choices, default=Config.Country.IT)
    language = serializers.ChoiceField(choices=Config.Language.choices, default=Config.Language.EN)
    ui_pref = serializers.ChoiceField(choices=Config.UIMode.choices, default=Config.UIMode.A)
