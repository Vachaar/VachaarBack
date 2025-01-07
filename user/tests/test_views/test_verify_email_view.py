from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.exceptions import UserNotFoundException
from user.tests.factories.user_factory import UserFactory
from user.views.register_view import VerifyEmailView


class VerifyEmailViewTests(TestCase):
    def test_verify_email_view_email_is_not_valid(self):
        # Arrange
        client = APIClient()
        data = {"code": "123456"}  # Missing email
        url = reverse("verify-email")

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_view_verification_code_is_required(self):
        # Arrange
        client = APIClient()
        data = {"email": "test@example.com"}  # Missing code
        url = reverse("verify-email")

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_view_user_not_found(self):
        # Arrange
        client = APIClient()
        data = {"email": "nonexistent@example.com", "code": "123456"}
        url = reverse("verify-email")

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["message"], UserNotFoundException.default_detail
        )

    def test_verify_email_view_verification_code_is_not_valid(self):
        # Arrange
        client = APIClient()
        email = "test@example.com"
        user = UserFactory(
            email=email,
            verification_code="123456",
            verification_code_expires_at="2099-12-31T23:59:59Z",
        )
        data = {"email": email, "code": "wrongcode"}
        url = reverse("verify-email")

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_view_successfully_verified(self):
        # Arrange
        client = APIClient()
        email = "test@example.com"
        user = UserFactory(
            email=email,
            verification_code="123456",
            verification_code_expires_at="2099-12-31T23:59:59Z",
        )
        data = {"email": email, "code": "123456"}
        url = reverse("verify-email")

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), VerifyEmailView.VERIFY_EMAIL_SUCCESS_MSG
        )
        self.assertIn("access", response.cookies)
        self.assertIn("refresh", response.cookies)

        user.refresh_from_db()

        self.assertTrue(user.is_email_verified)

        self.assertIsNone(user.verification_code)

        self.assertIsNone(user.verification_code_expires_at)
