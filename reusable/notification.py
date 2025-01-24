import random
import string
from abc import ABCMeta, abstractmethod
from datetime import timedelta
from typing import Optional

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from reusable.exceptions import EmailCanNotBeSentException
from user.models.user import User


class SingletonABCMeta(ABCMeta):
    """
    A metaclass that combines Singleton behavior and ABCMeta for abstract classes.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class EmailSender(metaclass=SingletonABCMeta):
    """
    Abstract base class for sending emails using the Form Template Method pattern.
    """

    @classmethod
    def prepare_email_message(
        cls, subject: str, message: str, recipient_email: str
    ) -> EmailMessage:
        return EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )

    def send_email(self, user: User, reason: Optional[str] = None):
        """
        Template method for sending emails.
        It defines the common steps while allowing customization through hooks.
        """
        subject = self.get_subject()
        message = self.get_message(user, reason)

        try:
            email = self.prepare_email_message(
                subject=subject,
                message=message,
                recipient_email=user.email,
            )
            email.send()
        except Exception:
            raise EmailCanNotBeSentException()

    @abstractmethod
    def get_subject(self) -> str:
        """
        Method to be implemented by subclasses to define the email subject.
        """
        pass

    @abstractmethod
    def get_message(self, user: User, reason: Optional[str]) -> str:
        """
        Method to be implemented by subclasses to define the email message.
        """
        pass


class BanUserEmailSender(EmailSender):
    def get_subject(self) -> str:
        return " -- Vachaar -- Ban Announcement --"

    def get_message(self, user: User, reason: Optional[str]) -> str:
        return f"""
        Unfortunately, you were banned because of the following reason:
        -- {reason} --

        For more information, please contact us!
        """


class BanItemEmailSender(EmailSender):
    def get_subject(self) -> str:
        return " -- Vachaar -- Ban Announcement --"

    def get_message(self, user: User, reason: Optional[str]) -> str:
        return f"""
        Unfortunately, your item was banned because of the following reason:
        -- {reason} --

        For more information, please contact us!
        """


class VerificationEmailSender(EmailSender):
    EMAIL_EXPIRY_MINUTES = 5

    def get_subject(self) -> str:
        return " -- Vachaar -- Email Verification Code --"

    def get_message(self, user: User, reason: Optional[str]) -> str:
        code = self.set_verification_code(user)
        return f"Your email verification code is {code}. This code will expire in {self.EMAIL_EXPIRY_MINUTES} minutes!"

    def set_verification_code(self, user: User) -> str:
        code = "".join(random.choices(string.digits, k=6))
        user.verification_code = code
        user.verification_code_expires_at = timezone.now() + timedelta(
            minutes=self.EMAIL_EXPIRY_MINUTES
        )
        user.save()
        return code
