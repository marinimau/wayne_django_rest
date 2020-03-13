from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile


class UserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField()


class ProfileSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

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
