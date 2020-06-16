from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ResetPasswordToken
from .tokens import password_reset_token
from .validators import change_password_validator
from api.user.validators import user_validators
from api.user.utils import send_reset_password_email, send_reset_password__confirm_email


# ----------------------------------------------------------------------------------------------------------------------
#
# ResetPasswordTokenSerializer
#
# - only creation
#
# ----------------------------------------------------------------------------------------------------------------------

class ResetPasswordTokenSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        error = {'message': 'no update request for this model'}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        email = validated_data.get('email', None)
        if user_validators.check_if_exist_email(email):
            user = User.objects.get(email=email)
            change_password_validator.check_if_already_exists_and_delete_token(user)
            token = password_reset_token.make_token(user)
            ip = validated_data.get('ip', None)
            user_agent = validated_data.get('user_agent', None)
            creation_timestamp = timezone.now()
            token_created = ResetPasswordToken.objects.create(user=user, email=email, token=token, ip=ip,
                                                              user_agent=user_agent,
                                                              creation_timestamp=creation_timestamp)
            token_created.save()
            # send email
            send_reset_password_email(user, ip, user_agent, token)
            return token_created
        else:
            error = {'message': 'invalid email'}
            raise serializers.ValidationError(error)

    user = serializers.ReadOnlyField(source='user.pk')
    email = serializers.CharField(max_length=50, required=True)
    token = serializers.CharField(max_length=50, read_only=True)
    ip = serializers.CharField(max_length=15, read_only=True)
    user_agent = serializers.CharField(max_length=100, read_only=True)
    creation_timestamp = serializers.DateTimeField(read_only=True)


# ----------------------------------------------------------------------------------------------------------------------
#
# AlterPasswordByTokenSerializer
#
# - only creation
#
# ----------------------------------------------------------------------------------------------------------------------

class AlterPasswordByTokenSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        error = {'message': 'no update request for this model'}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        email = validated_data.get('email', None)
        if user_validators.check_if_exist_email(email):
            user = User.objects.get(email=email)
            token_stored = change_password_validator.get_token_by_user(user)
            # check token
            change_password_validator.compare_and_validate_tokens(token_stored, validated_data)
            # if token is ok
            user_validators.update_password(user, validated_data)
            # if password is update delete token
            ResetPasswordToken.objects.filter(pk=token_stored.pk).delete()
            user.save()
            send_reset_password__confirm_email(user)
            success = {'message': 'password modified'}
            return token_stored
        else:
            error = {'message': 'invalid email'}
            raise serializers.ValidationError(error)

    token = serializers.CharField(max_length=40, required=True)
    email = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True, required=False)
    password2 = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True, required=False)