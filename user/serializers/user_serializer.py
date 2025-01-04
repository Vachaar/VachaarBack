from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models.user import User
from user.services.validators import UserValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "email", "password"]
        extra_kwargs = {
            "email": {
                "validators": [],
            },
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        existing_user = User.objects.filter(email=value).first()

        if existing_user:
            if existing_user.is_email_verified:
                raise serializers.ValidationError(
                    "User with this email already exists."
                )
            else:
                self.instance = existing_user

        UserValidator.email_validator(value)
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
