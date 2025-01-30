from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from user.exceptions import UserNotFoundException, EmailAlreadyVerifiedException
from user.tests.factories.user_factory import UserFactory
from user.views.register_view import ResendVerificationEmailCodeView


class TestResendVerificationEmailCode(TestCase):
    def test_resend_verification_email_code_successful(self):
        # Arrange
        email = "test@example.com"
        user = UserFactory(email=email, is_email_verified=False)
        factory = APIRequestFactory()
        url = reverse("resend-verification-email")

        # Act
        request = factory.post(url, {"email": email})
        response = ResendVerificationEmailCodeView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            ResendVerificationEmailCodeView.EMAIL_RESENT_SUCCESS_MSG,
        )

    def test_resend_verification_email_code_user_not_found(self):
        # Arrange
        email = "notfound@example.com"
        factory = APIRequestFactory()
        url = reverse("resend-verification-email")

        # Act
        request = factory.post(url, {"email": email})
        response = ResendVerificationEmailCodeView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], UserNotFoundException.default_detail
        )

    def test_resend_verification_email_code_email_already_verified(self):
        # Arrange
        email = "verified@example.com"
        user = UserFactory(email=email, is_email_verified=True)
        factory = APIRequestFactory()
        url = reverse("resend-verification-email")

        # Act
        request = factory.post(url, {"email": email})
        response = ResendVerificationEmailCodeView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["message"]),
            str(EmailAlreadyVerifiedException.default_detail),
        )
