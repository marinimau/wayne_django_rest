from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile


class UserSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField()


class ProfileSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.cellular = validated_data.get('cellular', instance.cellular)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.country = validated_data.get('country', instance.country)
        instance.language = validated_data.get('language', instance.language)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    user = UserSerializer()
    bio = serializers.CharField(max_length=500)
    location = serializers.CharField(max_length=200)
    cellular = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    surname = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=1)
    country = serializers.CharField(max_length=2)
    language = serializers.CharField(max_length=2)
    birth_date = serializers.CharField()
