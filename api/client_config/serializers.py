from rest_framework import serializers
from .validators.config_validators import validate_country, validate_language, validate_ui_pref

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
        error = {'message': 'config instance is created only with user creation'}
        raise serializers.ValidationError(error)

    user = serializers.ReadOnlyField(source='user.pk')
    country = serializers.CharField(max_length=2, allow_blank=True, required=False)
    language = serializers.CharField(max_length=2, allow_blank=True, required=False)
    ui_pref = serializers.CharField(allow_blank=True, required=False)