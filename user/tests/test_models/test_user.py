from django.core.exceptions import ValidationError
from django.test import TestCase

from user.models.user import User
from user.tests.factories.user_factory import UserFactory


class UserTestCase(TestCase):
    def test_get_user_by_email_existing_user(self):
        # Arrange
        email = "test@example.com"
        user = UserFactory(email=email)

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

        with self.assertRaises(ValidationError):
            UserFactory(email=invalid_email)

        # Act
        result = User.get_user_by_email(invalid_email)

        # Assert
        self.assertIsNone(result)
