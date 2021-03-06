#
#   wayne_django_rest copyright © 2020 - all rights reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from contents.messages.get_messages import get_messages
from django.conf import settings
from api.client_config.models import Config
from api.user.models import Profile
from api.utils import send_confirm_registration_email
from .validators import profile_validators, user_validators


messages = get_messages(package=settings.CONTENT_PACKAGES[0])


# ----------------------------------------------------------------------------------------------------------------------
#
# UserSerializer
#
# - update field {email, username, name and surname, deactivate_account, password}
# - create a user
#
# ----------------------------------------------------------------------------------------------------------------------

class UserSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        # email
        user_validators.update_email(instance, validated_data)
        # username
        user_validators.update_username(instance, validated_data)
        # name and surname
        user_validators.update_name_and_surname(instance, validated_data)
        # deactivate account
        user_validators.deactivate_account(instance, validated_data)
        # update password
        user_validators.update_password(instance, validated_data)
        instance.save()
        return instance

    def create(self, validated_data):
        date_joined = timezone.now()
        email = validated_data.pop('email', None)
        username = validated_data.pop('username', None)
        # check input
        result, msg = user_validators.check_input(email, username)
        if not result:
            raise serializers.ValidationError(msg)
        # check passwords
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        result, msg = user_validators.check_password(password, password2)
        if not result:
            raise serializers.ValidationError(msg)
        # if there are no errors
        user_created = User.objects.create(email=email, username=username.lower(), is_active=False,
                                           date_joined=date_joined, **validated_data)
        Profile.objects.create(user=user_created, email_confirmed=False)
        Config.objects.create(user=user_created)

        user_created.set_password(password)
        user_created.save()
        # send email
        send_confirm_registration_email(user_created)
        return user_created

    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=30, required=False)
    is_active = serializers.BooleanField(read_only=True, required=False)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False)
    password = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True, required=False)
    password2 = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True, required=False)


# ----------------------------------------------------------------------------------------------------------------------
#
# Profile serializer
#
# - update field (bio, location, cellular, gender, birth date)
#
# ----------------------------------------------------------------------------------------------------------------------


class ProfileSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        # validate bio
        profile_validators.validate_bio(instance, validated_data)
        # validate location
        profile_validators.validate_location(instance, validated_data)
        # validate cellular
        profile_validators.validate_cellular(instance, validated_data)
        # validate profile img
        profile_validators.validate_profile_img(instance, validated_data)
        # validate gender
        profile_validators.validate_gender(instance, validated_data)
        # validate birth_date
        profile_validators.validate_birth_date(instance, validated_data)
        instance.save()
        return instance

    def create(self, validated_data):
        error = {'message': messages['no_creation_for_profile_model_error']}
        raise serializers.ValidationError(error)

    # user = UserSerializer()
    user = serializers.ReadOnlyField(source='user.pk')
    bio = serializers.CharField(max_length=500, allow_blank=True, required=False)
    location = serializers.CharField(max_length=200, allow_blank=True, required=False)
    cellular = serializers.CharField(max_length=50, allow_blank=True, required=False)
    gender = serializers.ChoiceField(choices=Profile.Gender.choices, default=Profile.Gender.UNSPECIFIED)
    birth_date = serializers.CharField(allow_blank=True, required=False)
    url_img_profile = serializers.URLField(allow_blank=True, required=False)
    email_confirmed = serializers.BooleanField(default=False, read_only=True)
