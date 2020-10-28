#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.utils import timezone
from rest_framework import serializers
from .models import SocialAccountUsername, SocialAccountEmail
import api.social.validators.social_account_generic_validator as generic_validators
import api.social.validators.social_account_username_validator as username_account_validators
import api.social.validators.social_account_email_validators as email_account_validators


class SocialAccountSerializer(serializers.Serializer):
    # ------------------------------------------------------------------------------------------------------------------
    # SocialAccount serializer (abstract)
    # this is the serializer of the class Social Account
    # ------------------------------------------------------------------------------------------------------------------
    class Meta:
        abstract = True

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = generic_validators.validate_user(self.context)
        creation_timestamp = timezone.now()
        return user, creation_timestamp

    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.pk')
    required = serializers.BooleanField(read_only=True, default=False)
    creation_timestamp = serializers.DateTimeField(read_only=True, required=False)


class SocialAccountUsernameSerializer(SocialAccountSerializer):
    # ------------------------------------------------------------------------------------------------------------------
    # SocialAccountUsernameSerializer
    # this is the serializer of the class Social Account Username
    # the editable fields are:
    # - value
    # ------------------------------------------------------------------------------------------------------------------
    def update(self, instance, validated_data):
        username_account_validators.update_value(instance, validated_data.pop('value', instance.value))
        return instance

    def create(self, validated_data):
        user, creation_timestamp = super().create(validated_data)
        platform, value = username_account_validators.validate_user_account_creation(validated_data)
        SocialAccountUsername.objects.create(user=user, creation_timestamp=creation_timestamp, platform=platform,
                                             value=str.lower(value))

    platform = serializers.ChoiceField(required=True,
                                       choices=SocialAccountUsername.UsernamePlatforms.choices)
    value = serializers.CharField(max_length=50, required=True)


class SocialAccountEmailSerializer(SocialAccountSerializer):
    # ------------------------------------------------------------------------------------------------------------------
    # SocialAccountEmailSerializer
    # this is the serializer of the class Social Account Username
    # the editable fields are:
    # - value
    # ------------------------------------------------------------------------------------------------------------------
    def update(self, instance, validated_data):
        email_account_validators.update_value(instance, validated_data.pop('value', instance.value))
        return instance

    def create(self, validated_data):
        user, creation_timestamp = super().create(validated_data)
        platform, value = email_account_validators.validate_email_account_creation(validated_data)
        SocialAccountEmail.objects.create(user=user, creation_timestamp=creation_timestamp, platform=platform,
                                          value=value)

    platform = serializers.ChoiceField(required=True,
                                       choices=SocialAccountEmail.EmailProviders.choices)
    value = serializers.CharField(max_length=50, required=True)
