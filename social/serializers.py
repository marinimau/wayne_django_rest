from django.utils import timezone
from rest_framework import serializers
from .models import SocialLabel, SocialAccount



# ----------------------------------------------------------------------------------------------------------------------
# Label
# ----------------------------------------------------------------------------------------------------------------------

def check_if_exists_label(title, user):
    return SocialLabel.objects.filter(title=title).filter(user=user).count() != 0


def validate_title(title, user):
    return (not check_if_exists_label(title, user)) and 3 < len(title) <= 20


def validate_privacy(privacy):
    return privacy in dict(SocialLabel.LabelPrivacyConfig.choices)


class LabelSerializer(serializers.Serializer):
    # ------------------------------------------------------------------------------------------------------------------
    # LabelSerializer
    # this is the serializer of the class label
    # the editable fields are:
    # - privacy: {public, friends, strict, private}
    # - title: string
    # ------------------------------------------------------------------------------------------------------------------
    def update(self, instance, validated_data):
        error = {'message': 'no update request for this model'}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        title = validated_data.get('title', None)
        user = validated_data.get('user', None)
        privacy = validated_data.get('privacy', None).upper()
        validate_privacy(privacy)
        if validate_title(title, user) and user is not None:
            label_created = SocialLabel.objects.create(title=title.lower(), user=user,
                                                       privacy=privacy, required=False,
                                                       creation_timestamp=timezone.now())
            label_created.save()
            return label_created
        else:
            error = {'message': 'error - label creation failed'}
            raise serializers.ValidationError(error)

    id = serializers.ReadOnlyField(read_only=True)
    user = serializers.ReadOnlyField(source='user.pk', read_only=True)
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