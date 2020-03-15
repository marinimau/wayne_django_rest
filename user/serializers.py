from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile
from user.utils import send_confirm_registration_email


class UserSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        # username
        username = validated_data.get('username', instance.username)
        instance.username = username.lower()
        # name and surname
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # deactivate account - one way
        is_active = validated_data.get('is_active', instance.is_active)
        if is_active is False and is_active != instance.is_active:
            instance.is_active = is_active
        # alter password
        password = validated_data.get('password', None)
        password2 = validated_data.get('password2', None)
        if password is not None and password == password2:
            instance.set_password(raw_password=password)
        instance.save()
        return instance

    def create(self, validated_data):
        date_joined = timezone.now()
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password == password2:
            user_created = User.objects.create(username=username.lower(), is_active=False, date_joined=date_joined, **validated_data)
            Profile.objects.create(user=user_created, email_confirmed=False)
            user_created.set_password(password)
            user_created.save()
            # send email
            send_confirm_registration_email(user_created)
            return user_created
        else:
            error = {'message': 'password mismatch'}
            raise serializers.ValidationError(error)

    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=30, required=False)
    is_active = serializers.BooleanField(read_only=True, required=False)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False)
    password = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True, required=False)
    password2 = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True, required=False)


class ProfileSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.cellular = validated_data.get('cellular', instance.cellular)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.country = validated_data.get('country', instance.country)
        instance.language = validated_data.get('language', instance.language)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.ui_pref = validated_data.get('ui_pref', instance.ui_pref)
        instance.save()
        return instance

    def create(self, validated_data):
        validated_data.pop('email_confirmed')
        return Profile.objects.create(email_confirmed=False, **validated_data)

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



