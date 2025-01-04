from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken

from user.models.user import User
from user.serializers.user_serializer import CustomTokenObtainPairSerializer
from user.serializers.user_serializer import UserRegistrationSerializer
from user.tests.factories.user_factory import UserFactory


class TestCustomTokenObtainPairSerializer(TestCase):
    def test_get_token_includes_email(self):
        # Arrange
        user = UserFactory()

        serializer = CustomTokenObtainPairSerializer()

        # Act
        refresh = RefreshToken.for_user(user)
        token = serializer.get_token(user)

        # Assert
        self.assertIn("email", token)
        self.assertEqual(token["email"], user.email)


class TestUserRegistrationSerializer(TestCase):
    def test_user_registration_serializer_with_valid_data(self):
        # Arrange
        valid_data = {
            "email": "test@example.com",
            "phone": "09123456789",
            "password": "securepassword",
        }

        serializer = UserRegistrationSerializer(data=valid_data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertTrue(is_valid)
        user = serializer.save()
        self.assertEqual(user.email, valid_data["email"])
        self.assertEqual(user.phone, valid_data["phone"])

    def test_user_registration_serializer_with_missing_fields(self):
        # Arrange
        invalid_data = {
            "email": "test@example.com",
            # Missing phone and password fields
        }

        serializer = UserRegistrationSerializer(data=invalid_data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn("phone", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_user_registration_serializer_with_invalid_email(self):
        # Arrange
        invalid_data = {
            "email": "not-an-email",
            "phone": "1234567890",
            "password": "securepassword",
        }

        serializer = UserRegistrationSerializer(data=invalid_data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn("email", serializer.errors)

    def test_user_registration_serializer_with_blank_fields(self):
        # Arrange
        invalid_data = {
            "email": "",
            "phone": "",
            "password": "",
        }

        serializer = UserRegistrationSerializer(data=invalid_data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn("email", serializer.errors)
        self.assertIn("phone", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_user_registration_serializer_with_duplicate_email(self):
        # Arrange
        UserFactory(
            email="duplicate@example.com",
            phone="09123456789",
            password="securepassword",
        )
        duplicate_data = {
            "email": "duplicate@example.com",
            "phone": "09123456789",
            "password": "anotherpassword",
        }

        serializer = UserRegistrationSerializer(data=duplicate_data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertTrue(is_valid)
