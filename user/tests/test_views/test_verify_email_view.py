from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from user.exceptions import UserNotFoundException
from user.tests.factories.user_factory import UserFactory
from user.views.register_view import VerifyEmailView


class VerifyEmailViewTests(TestCase):
    def test_verify_email_view_email_is_not_valid(self):
        # Arrange
        factory = APIRequestFactory()
        data = {"code": "123456"}  # Missing email
        url = reverse("verify-email")

        # Act
        request = factory.post(url, data)
        response = VerifyEmailView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_view_verification_code_is_required(self):
        # Arrange
        factory = APIRequestFactory()
        data = {"email": "test@example.com"}  # Missing code
        url = reverse("verify-email")

        # Act
        request = factory.post(url, data)
        response = VerifyEmailView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_view_user_not_found(self):
        # Arrange
        factory = APIRequestFactory()
        data = {"email": "nonexistent@example.com", "code": "123456"}
        url = reverse("verify-email")

        # Act
        request = factory.post(url, data)
        response = VerifyEmailView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], UserNotFoundException.default_detail
        )

    def test_verify_email_view_verification_code_is_not_valid(self):
        # Arrange
        factory = APIRequestFactory()
        email = "test@example.com"
        user = UserFactory(
            email=email,
            verification_code="123456",
            verification_code_expires_at="2099-12-31T23:59:59Z",
        )
        data = {"email": email, "code": "wrongcode"}
        url = reverse("verify-email")

        # Act
        request = factory.post(url, data)
        response = VerifyEmailView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
