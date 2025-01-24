from reusable.notification import VerificationEmailSender
from user.models.user import User


def send_verification_email(user: User):
    # Send verification email
    VerificationEmailSender().send_email(user)
