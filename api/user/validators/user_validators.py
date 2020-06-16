import re
from rest_framework import serializers
from django.contrib.auth.models import User


# ----------------------------------------------------------------------------------------------------------------------
# User validators
# - password
# - account deactivation
# - email
# - username
# - password reset
# - name and surname
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# evaluate the password strength
# ----------------------------------------------------------------------------------------------------------------------
def check_password_strength(password):
    return re.search("^(?=.*[A-Z])(?=.*[!@#$&*.\-_])(?=.*[0-9])(?=.*[a-z]).{8,40}$", password)


# ----------------------------------------------------------------------------------------------------------------------
# evaluate the passowrd (security and matching)
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# password update
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# deactivate account
# ----------------------------------------------------------------------------------------------------------------------
def deactivate_account(instance, validated_data):
    # deactivate account - one way
    is_active = validated_data.get('is_active', instance.is_active)
    if is_active is False and is_active != instance.is_active:
        instance.is_active = is_active
    return


# ----------------------------------------------------------------------------------------------------------------------
# check if exists email
# ----------------------------------------------------------------------------------------------------------------------
def check_if_exist_email(email):
    return User.objects.filter(email=email).count() != 0


# ----------------------------------------------------------------------------------------------------------------------
# update email
# ----------------------------------------------------------------------------------------------------------------------
def update_email(instance, validated_data):
    email = validated_data.get('email', instance.email)
    if email != instance.email:
        if not check_if_exist_email(email):
            instance.email = email
        else:
            error = {'message': 'email already used'}
            raise serializers.ValidationError(error)
    return


# ----------------------------------------------------------------------------------------------------------------------
# check if exists username
# ----------------------------------------------------------------------------------------------------------------------
def check_if_exist_username(username):
    return User.objects.filter(username=username).count() != 0


# ----------------------------------------------------------------------------------------------------------------------
# update username
# ----------------------------------------------------------------------------------------------------------------------
def update_username(instance, validated_data):
    username = validated_data.get('username', instance.username)
    if username.lower() != instance.username.lower():
        if not check_if_exist_username(username):
            instance.username = username.lower()
        else:
            error = {'message': 'username already used'}
            raise serializers.ValidationError(error)
    return


# ----------------------------------------------------------------------------------------------------------------------
# update name and surname
# ----------------------------------------------------------------------------------------------------------------------
def update_name_and_surname(instance, validated_data):
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    return


# ----------------------------------------------------------------------------------------------------------------------
# check input for user update and registration
# ----------------------------------------------------------------------------------------------------------------------
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
