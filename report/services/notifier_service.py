from reusable.notification import BanUserEmailSender, BanItemEmailSender
from user.models.user import User


def send_ban_user_email(user: User, reason: str) -> None:
    # Send ban user email
    BanUserEmailSender().send_email(user, reason=reason)


def send_ban_item_email(user: User, reason: str) -> None:
    # Send ban item email
    BanItemEmailSender().send_email(user, reason=reason)
