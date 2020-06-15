from ..models import Profile
from rest_framework import serializers
import re
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------
#
#   Profile validatos
#       - location
#       - bio
#       - cellular
#       - gender
#       - birth date
#
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# validate location
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# validate bio
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


# ----------------------------------------------------------------------------------------------------------------------
# validate cellular
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# validate gender
# ----------------------------------------------------------------------------------------------------------------------
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


def validate_birth_date(instance, validated_data):
    birth_date = validated_data.get('birth_date', instance.birth_date)
    if birth_date != instance.birth_date:
        # if the request edit language field
        try:
            date_clean = datetime.strptime(birth_date, '%Y-%m-%d')
        except serializers.ValidationError:
            error = {'message': 'invalid date format in birth_date'}
            raise serializers.ValidationError(error)
        # if format is valid
        if date_clean is not None and (datetime.now() - date_clean).days / 365 >= 16:
            instance.birth_date = birth_date
            return
        else:
            error = {'message': 'invalid birth_date, You must be at least 16 years old to register.'}
            raise serializers.ValidationError(error)
