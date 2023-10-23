from typing import Any, Dict

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    RefreshToken,
)
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login

from .models import User


class UserRegistrationSerilizer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['phone_number', 'password', 'confirm_password',
                  'first_name', 'last_name', 'email']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "password fields didn't match."})
        if len(attrs['password']) > 20:
            raise serializers.ValidationError({"password": ('''password is too long, 
                                                            maximum length 20 characters!''')})
        if (attrs['email'] == '' and attrs['phone_number'] == ''):
            raise serializers.ValidationError({"fields": "one of email or phone number fields must be set."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "password fields didn't match."})
        if len(attrs['new_password']) > 20:
            raise serializers.ValidationError({"new_password": ("password is too long, maximum length 20 characters!")})
        return attrs
