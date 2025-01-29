from unittest.mock import patch, MagicMock

from django.core.mail import EmailMessage
from django.test import TestCase

from reusable.exceptions import EmailCanNotBeSentException
from user.services.register_email_service import send_verification_email
from user.tests.factories.user_factory import UserFactory


class TestRegisterEmailService(TestCase):
    def test_send_verification_email_success(self):
        user = UserFactory()
        mock_email_message = MagicMock(spec=EmailMessage)

        with patch(
            "reusable.notification.EmailSender.prepare_email_message",
            return_value=mock_email_message,
        ) as prepare_email_mock:
            # Act
            send_verification_email(user)

            # Assert
            prepare_email_mock.assert_called_once()
            mock_email_message.send.assert_called_once()

    def test_send_verification_email_raises_exception(self):
        # Arrange
        user = UserFactory()

        with patch(
            "reusable.notification.EmailSender.prepare_email_message",
            side_effect=Exception,
        ) as prepare_email_mock:
            # Act and Assert
            self.assertRaises(
                EmailCanNotBeSentException, send_verification_email, user
            )

            prepare_email_mock.assert_called_once()
