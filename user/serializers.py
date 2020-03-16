from datetime import datetime
import re

from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile
from user.utils import send_confirm_registration_email


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
    return re.search("^(?=.*[A-Z])(?=.*[!@#$&*.-_])(?=.*[0-9])(?=.*[a-z]).{8,40}$", password)


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
    instance.email = validated_data.get('email', instance.email)
    return


def update_username(instance, validated_data):
    username = validated_data.get('username', instance.username)
    instance.username = username.lower()
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


def check_password(password, password2):
    if password is None:
        error = {'message': 'input error'}
        return False, error
    elif not check_password_strength(password):
        error = {'message': 'password unsecure'}
        return False, error
    elif password != password2:
        error = {'message': 'password mismatch'}
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
#   Profile management
#       -update field
#       -data manipulation
#       -validators for each field
#
# ----------------------------------------------------------------------------------------------------------------------

def validate_bio(instance, validated_data):
    bio = validated_data.get('bio', instance.bio)
    if bio != instance.bio:
        # if the request edit bio field
        if len(bio) <= 200:
            instance.bio = bio
            return
        else:
            error = {'message': 'bio is too long'}
            raise serializers.ValidationError(error)


def validate_cellular(instance, validated_data):
    cellular = validated_data.get('cellular', instance.cellular)
    if cellular != instance.cellular:
        # if the request edit cellular field
        if re.search("^\+[0-9]{2,3} [0-9]{6,13}$", cellular):
            instance.cellular = cellular
            return
        else:
            error = {'message': 'invalid cellular number format'}
            raise serializers.ValidationError(error)


def validate_location(instance, validated_data):
    location = validated_data.get('location', instance.location)
    if location != instance.location:
        # if the request edit cellular field
        if len(location) <= 20:
            instance.location = location
            return
        else:
            error = {'message': 'invalid location'}
            raise serializers.ValidationError(error)


def validate_gender(instance, validated_data):
    gender = validated_data.get('gender', instance.gender).upper()
    if gender != instance.gender:
        # if the request edit gender field
        if gender in dict(Profile.Gender.choices):
            instance.gender = gender
            return
        else:
            error = {'message': 'invalid value for gender'}
            raise serializers.ValidationError(error)


def validate_country(instance, validated_data):
    country = validated_data.get('country', instance.country).upper()
    if country != instance.country:
        # if the request edit language field
        if country in dict(Profile.Country.choices):
            instance.country = country
            return
        else:
            error = {'message': 'invalid value for country'}
            raise serializers.ValidationError(error)


def validate_language(instance, validated_data):
    language = validated_data.get('language', instance.language).upper()
    if language != instance.language:
        # if the request edit language field
        if language in dict(Profile.Language.choices):
            instance.language = language
            return
        else:
            error = {'message': 'invalid value for language'}
            raise serializers.ValidationError(error)


def validate_birth_date(instance, validated_data):
    birth_date = validated_data.get('birth_date', instance.birth_date)
    if birth_date != instance.birth_date:
        # if the request edit language field
        try:
            date_clean = datetime.strptime(birth_date, '%Y-%m-%d')
        except serializers.ValidationError:
            date_clean = None
            error = {'message': 'invalid date format in birth_date'}
            raise serializers.ValidationError(error)
        # if format is valid
        if date_clean is not None and (datetime.now() - date_clean).days/365 >= 16:
            instance.birth_date = birth_date
            return
        else:
            error = {'message': 'invalid birth_date, You must be at least 16 years old to register.'}
            raise serializers.ValidationError(error)


def validate_ui_pref(instance, validated_data):
    ui_pref = validated_data.get('ui_pref', instance.ui_pref).upper()
    if ui_pref != instance.ui_pref:
        # if the request edit language field
        if ui_pref in dict(Profile.UIMode.choices):
            instance.ui_pref = ui_pref
            return
        else:
            error = {'message': 'invalid choice for UI pref'}
            raise serializers.ValidationError(error)


class ProfileSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        # validate bio
        validate_bio(instance, validated_data)
        # validate location
        validate_location(instance, validated_data)
        # validate cellular
        validate_cellular(instance, validated_data)
        # validate gender
        validate_gender(instance, validated_data)
        # validate country
        validate_country(instance, validated_data)
        # validate language
        validate_language(instance, validated_data)
        # validate birth_date
        validate_birth_date(instance, validated_data)
        # validate ui_pref
        validate_ui_pref(instance, validated_data)
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
    country = serializers.CharField(max_length=2, allow_blank=True, required=False)
    language = serializers.CharField(max_length=2, allow_blank=True, required=False)
    ui_pref = serializers.CharField(allow_blank=True, required=False)
    birth_date = serializers.CharField(allow_blank=True, required=False)
    email_confirmed = serializers.BooleanField(required=False)
