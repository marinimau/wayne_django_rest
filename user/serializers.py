from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile


class UserSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        return instance

    def create(self, validated_data):
        date_joined = timezone.now()
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password == password2:
            user_created = User.objects.create(username=username.lower(), is_active=False, date_joined=date_joined, **validated_data)
            user_created.set_password(password)
            user_created.save()
            return user_created
        else:
            error = {'message': 'password mismatch'}
            raise serializers.ValidationError(error)

    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    is_active = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, max_length=50, write_only=True)


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
        return Profile.objects.create(email_confirmed=False, **validated_data)

    # user = UserSerializer()
    user = serializers.ReadOnlyField(source='user.pk')
    bio = serializers.CharField(max_length=500)
    location = serializers.CharField(max_length=200)
    cellular = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=1)
    country = serializers.CharField(max_length=2)
    language = serializers.CharField(max_length=2)
    ui_pref = serializers.CharField()
    birth_date = serializers.CharField()
    email_confirmed = serializers.BooleanField()
