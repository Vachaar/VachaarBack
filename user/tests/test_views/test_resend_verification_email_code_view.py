from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.exceptions import UserNotFoundException, EmailAlreadyVerifiedException
from user.tests.factories.user_factory import UserFactory


class TestResendVerificationEmailCode(TestCase):
    def test_resend_verification_email_code_successful(self):
        # Arrange
        email = "test@example.com"
        user = UserFactory(email=email, is_email_verified=False)
        client = APIClient()
        url = reverse("resend-verification-email")

        # Act
        response = client.post(url, {"email": email})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"detail": "Email verification code resent successfully."},
        )

    def test_resend_verification_email_code_user_not_found(self):
        # Arrange
        email = "notfound@example.com"
        client = APIClient()
        url = reverse("resend-verification-email")

        # Act
        response = client.post(url, {"email": email})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["message"], UserNotFoundException.default_detail
        )

    def test_resend_verification_email_code_email_already_verified(self):
        # Arrange
        email = "verified@example.com"
        user = UserFactory(email=email, is_email_verified=True)
        client = APIClient()
        url = reverse("resend-verification-email")

        # Act
        response = client.post(url, {"email": email})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.json()["message"]),
            str(EmailAlreadyVerifiedException.default_detail),
        )
