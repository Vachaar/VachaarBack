from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.exceptions import (
    PhoneIsNotValidException,
    EmailIsNotValidException,
    UserAlreadyExistsException,
)
from user.models.user import User
from user.services.validators import UserValidator


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length=128)
    phone = serializers.CharField()

    def validate_email(self, value):
        try:
            UserValidator.email_validator(value)
        except ValidationError:
            raise EmailIsNotValidException()

        existing_user = User.objects.filter(email=value).first()

        if existing_user:
            if existing_user.is_email_verified:
                raise UserAlreadyExistsException()
            else:
                self.instance = existing_user

        return value

    def validate_phone(self, value):
        try:
            UserValidator.phone_validator(value)
        except ValidationError:
            raise PhoneIsNotValidException()
        return value

    def create(self, validated_data):
        if self.instance:
            return self.update(self.instance, validated_data)
        else:
            return User.objects.create(
                email=validated_data["email"],
                phone=validated_data["phone"],
                password=validated_data["password"],
            )

    def update(self, instance, validated_data):
        instance.phone = validated_data["phone"]
        instance.set_password(validated_data["password"])
        instance.full_clean()
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        return token


class EditPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        try:
            UserValidator.phone_validator(value)
        except ValidationError:
            raise PhoneIsNotValidException()
        return value

    def update(self, user, validated_data):
        user.phone = validated_data["phone"]
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone"]
