import random
import string
from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from user.models.user import User


def set_verification_code(user: User):
    code = "".join(random.choices(string.digits, k=6))
    user.verification_code = code

    user.verification_code_expires_at = timezone.now() + timedelta(minutes=5)

    user.save()
    return code


def prepare_email_message(
    subject: str, message: str, recipient_email: str
) -> EmailMessage:
    return EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )


def send_verification_email(user: User):
    EMAIL_SUBJECT = " -- Vachaar -- Email Verification Code --"
    EMAIL_EXPIRY_MINUTES = 5

    code = set_verification_code(user=user)
    message = f"Your email verification code is {code}. This code will expire in {EMAIL_EXPIRY_MINUTES} minutes!"

    try:
        email = prepare_email_message(
            subject=EMAIL_SUBJECT,
            message=message,
            recipient_email=user.email,
        )
        email.send()
    except Exception as e:
        print(f"Failed to send verification email to {user.email}. Error: {e}")
