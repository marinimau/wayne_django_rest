from datetime import datetime
import re
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile, ResetPasswordToken
from client_config.models import Config
from user.tokens import password_reset_token
from .validators import profile_validators, user_validators, change_password_validator
from user.utils import send_confirm_registration_email, send_reset_password_email, send_reset_password__confirm_email


# ----------------------------------------------------------------------------------------------------------------------
#
#   User management
#       -registration
#       -data manipulation
#       -account deactivation
#       -profile creation
#       -password reset
#       -validators for each field
#       -email trigger
#
# ----------------------------------------------------------------------------------------------------------------------

def check_password_strength(password):
    return re.search("^(?=.*[A-Z])(?=.*[!@#$&*.\-_])(?=.*[0-9])(?=.*[a-z]).{8,40}$", password)


def check_password(password, password2):
    if password is None:
        error = {'message': 'input error'}
        return False, error
    elif not check_password_strength(password):
        error = {'message': 'password insecure'}
        return False, error
    elif password != password2:
        error = {'message': 'password mismatch'}
        return False, error
    else:
        return True, None


def update_password(instance, validated_data):
    # alter password
    password = validated_data.get('password', instance.password)
    password2 = validated_data.get('password2', instance.password)
    if password != instance.password:
        result, msg = check_password(password, password2)
        if result:
            instance.set_password(raw_password=password)
        else:
            raise serializers.ValidationError(msg)


def deactivate_account(instance, validated_data):
    # deactivate account - one way
    is_active = validated_data.get('is_active', instance.is_active)
    if is_active is False and is_active != instance.is_active:
        instance.is_active = is_active
    return


def update_email(instance, validated_data):
    email = validated_data.get('email', instance.email)
    if email != instance.email:
        if not check_if_exist_email(email):
            instance.email = email
        else:
            error = {'message': 'email already used'}
            raise serializers.ValidationError(error)
    return


def update_username(instance, validated_data):
    username = validated_data.get('username', instance.username)
    if username.lower() != instance.username.lower():
        if not check_if_exist_username(username):
            instance.username = username.lower()
        else:
            error = {'message': 'username already used'}
            raise serializers.ValidationError(error)
    return


def update_name_and_surname(instance, validated_data):
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    return


def check_if_exist_email(email):
    return User.objects.filter(email=email).count() != 0


def check_if_exist_username(username):
    return User.objects.filter(username=username).count() != 0


def check_input(email, username):
    if email is None or username is None:
        error = {'message': 'input error'}
        return False, error
    # check if email is already used
    elif check_if_exist_email(email):
        error = {'message': 'email already used'}
        return False, error
    # check if username is already used
    elif check_if_exist_username(username):
        error = {'message': 'username already used'}
        return False, error
    else:
        return True, None



class UserSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        # email
        update_email(instance, validated_data)
        # username
        update_username(instance, validated_data)
        # name and surname
        update_name_and_surname(instance, validated_data)
        # deactivate account
        deactivate_account(instance, validated_data)
        # update password
        update_password(instance, validated_data)
        instance.save()
        return instance

    def create(self, validated_data):
        date_joined = timezone.now()
        email = validated_data.pop('email', None)
        username = validated_data.pop('username', None)
        # check input
        result, msg = check_input(email, username)
        if not result:
            raise serializers.ValidationError(msg)
        # check passwords
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        result, msg = check_password(password, password2)
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
        # validate gender
        profile_validators.validate_gender(instance, validated_data)
        # validate birth_date
        profile_validators.validate_birth_date(instance, validated_data)
        instance.save()
        return instance

    def create(self, validated_data):
        error = {'message': 'profile instance is created only with user creation'}
        raise serializers.ValidationError(error)

    # user = UserSerializer()
    user = serializers.ReadOnlyField(source='user.pk')
    bio = serializers.CharField(max_length=500, allow_blank=True, required=False)
    location = serializers.CharField(max_length=200, allow_blank=True, required=False)
    cellular = serializers.CharField(max_length=50, allow_blank=True, required=False)
    gender = serializers.CharField(max_length=1, allow_blank=True, required=False)
    birth_date = serializers.CharField(allow_blank=True, required=False)
    email_confirmed = serializers.BooleanField(required=False, read_only=True)


# ----------------------------------------------------------------------------------------------------------------------
#
#   Reset password token serializer
#
# ----------------------------------------------------------------------------------------------------------------------
def check_if_already_exists_and_delete_token(user):
    ResetPasswordToken.objects.filter(user=user).delete()
    return


def get_token_by_user(user):
    if ResetPasswordToken.objects.filter(user=user).exists():
        return ResetPasswordToken.objects.get(user=user)
    else:
        error = {'message': 'no token for the given user'}
        raise serializers.ValidationError(error)


class ResetPasswordTokenSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        error = {'message': 'no update request for this model'}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        email = validated_data.get('email', None)
        if check_if_exist_email(email):
            user = User.objects.get(email=email)
            check_if_already_exists_and_delete_token(user)
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


def compare_and_validate_tokens(token_obj, validated_data):
    token_get = validated_data.get('token', None)
    if token_get is not None and token_obj.token == token_get:
        if token_obj.creation_timestamp is not None and (timezone.now() - token_obj.creation_timestamp).days <= 1:
            return True
        else:
            error = {'message': 'token expired'}
            raise serializers.ValidationError(error)
    else:
        error = {'message': 'invalid token'}
        raise serializers.ValidationError(error)


class AlterPasswordByTokenSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        error = {'message': 'no update request for this model'}
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        email = validated_data.get('email', None)
        if check_if_exist_email(email):
            user = User.objects.get(email=email)
            token_stored = get_token_by_user(user)
            # check token
            compare_and_validate_tokens(token_stored, validated_data)
            # if token is ok
            update_password(user, validated_data)
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
