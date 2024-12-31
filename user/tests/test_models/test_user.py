from django.core.exceptions import ValidationError
from django.test import TestCase

from user.models.user import User


class UserTestCase(TestCase):
    def test_get_user_by_email_existing_user(self):
        # Arrange
        email = "test@example.com"
        password = "testpassword"
        phone = "09123456789"
        user = User.objects.create(email=email, password=password, phone=phone)

        # Act
        result = User.get_user_by_email(email)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.email, email)
        self.assertEqual(result.sso_user_id, user.sso_user_id)

    def test_get_user_by_email_nonexistent_user(self):
        # Arrange
        email = "nonexistent@example.com"

        # Act
        result = User.get_user_by_email(email)

        # Assert
        self.assertIsNone(result)

    def test_get_user_by_email_invalid_email(self):
        # Arrange
        invalid_email = "invalid_email"
        password = "testpassword"
        phone = "09123456789"

        with self.assertRaises(ValidationError):
            User.objects.create(
                email=invalid_email, password=password, phone=phone
            )

        # Act
        result = User.get_user_by_email(invalid_email)

        # Assert
        self.assertIsNone(result)
