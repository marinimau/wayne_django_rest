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
from .models import SocialAccount


# ----------------------------------------------------------------------------------------------------------------------
# Label
# ----------------------------------------------------------------------------------------------------------------------

def check_if_exists_label(title, wall):
    return SocialLabel.objects.filter(title=title).filter(wall=wall).count() != 0


def validate_title(title, wall):
    return (not check_if_exists_label(title, wall)) and 3 < len(title) <= 20


class SocialAccountSerializer(serializers.Serializer):
    # ------------------------------------------------------------------------------------------------------------------
    # SocialAccount serializer
    # this is the serializer of the class Social Account
    # the editable fields are:
    # - value
    # ------------------------------------------------------------------------------------------------------------------
    def update(self, instance, validated_data):
        error = {'message': 'no update request for this model'}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        platform = validated_data.get('platform', None)
        user = validated_data.get('user', None).upper()
        value = validated_data.get('value', None)
        if validate_title(title, user) and user is not None:
            label_created = SocialLabel.objects.create(title=title.lower(), user=user, required=False,
                                                       creation_timestamp=timezone.now())
            label_created.save()
            return label_created
        else:
            error = {'message': 'error - label creation failed'}
            raise serializers.ValidationError(error)

    id = serializers.ReadOnlyField(read_only=True)
    wall = serializers.ReadOnlyField(read_only=True)
    title = serializers.CharField(max_length=20, required=True)
    privacy = serializers.CharField(max_length=10, required=False)
    required = serializers.ReadOnlyField(read_only=True)


# ----------------------------------------------------------------------------------------------------------------------
# Wall
# ----------------------------------------------------------------------------------------------------------------------

class SocialWallSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        error = {'message': 'error - no update for this model'}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        error = {'message': 'error - no create for this model'}
        raise serializers.ValidationError(error)

    user = serializers.ReadOnlyField(source='user.pk', read_only=True)
    labels = LabelSerializer(many=True, read_only=True)
