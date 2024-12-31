from datetime import timedelta
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.core.mail import EmailMessage
from django.test import TestCase
from django.utils import timezone

from user.models.user import User
from user.services.register_service import send_verification_email
from user.services.register_service import (
    set_verification_code,
    prepare_email_message,
)


class TestRegisterService(TestCase):
    def test_set_verification_code_sets_code_and_expiry(self):
        # Arrange
        email = "test@example.com"
        password = "testpassword"
        phone = "09123456789"
        user = User.objects.create(email=email, password=password, phone=phone)

        # Act
        code = set_verification_code(user)

        # Assert
        user.refresh_from_db()
        self.assertEqual(user.verification_code, code)

        self.assertIsNotNone(user.verification_code_expires_at)

        self.assertGreater(user.verification_code_expires_at, timezone.now())

    def test_set_verification_code_resets_previous_code_and_expiry(self):
        # Arrange
        user = User.objects.create(
            email="test2@example.com",
            password="testpassword",
            phone="09123456789",
            verification_code="123456",
            verification_code_expires_at=timezone.now() + timedelta(minutes=5),
        )

        # Act
        new_code = set_verification_code(user)

        # Assert
        user.refresh_from_db()
        self.assertEqual(user.verification_code, new_code)

        self.assertNotEqual(user.verification_code, "123456")

        self.assertGreater(user.verification_code_expires_at, timezone.now())

    def test_prepare_email_message_valid_data(self):
        # Arrange
        subject = "Test Subject"
        message = "This is a test message."
        recipient_email = "recipient@example.com"

        # Act
        email_message = prepare_email_message(subject, message, recipient_email)

        # Assert
        self.assertIsInstance(email_message, EmailMessage)

        self.assertEqual(email_message.subject, subject)

        self.assertEqual(email_message.body, message)

        self.assertEqual(email_message.from_email, settings.DEFAULT_FROM_EMAIL)

        self.assertIn(recipient_email, email_message.to)

    def test_send_verification_email_success(self):
        email = "test@example.com"
        password = "testpassword"
        phone = "09123456789"
        user = User.objects.create(email=email, password=password, phone=phone)
        mock_email_message = MagicMock(spec=EmailMessage)

        with patch(
            "user.services.register_service.prepare_email_message",
            return_value=mock_email_message,
        ) as prepare_email_mock:
            # Act
            send_verification_email(user)

            # Assert
            prepare_email_mock.assert_called_once()
            mock_email_message.send.assert_called_once()

    def test_send_verification_email_raises_exception(self):
        # Arrange
        email = "test@example.com"
        password = "testpassword"
        phone = "09123456789"
        user = User.objects.create(email=email, password=password, phone=phone)

        with patch(
            "user.services.register_service.prepare_email_message",
            side_effect=Exception,
        ) as prepare_email_mock:
            # Act and Assert
            send_verification_email(user)

            prepare_email_mock.assert_called_once()
