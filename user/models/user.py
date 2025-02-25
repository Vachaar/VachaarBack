from typing import Optional

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.services.validators import UserValidator


class UserManager(BaseUserManager):
    """
    UserManager is a custom manager class for the user model that provides utility
    methods for creating regular users and superusers.

    This class extends the BaseUserManager class and includes methods for
    streamlining the creation of users with hashed passwords while managing
    additional user fields. It also ensures input validation and proper normalization
    of required fields, such as email.

    :ivar _db: Database alias to use.
    :type _db: Any
    :ivar model: Reference to the user model associated with this manager.
    :type model: Type[Model]
    """

    def create(self, email: str, password: str, phone: str, **kwargs):
        user = self.model(email=email, phone=phone, **kwargs)
        user.username = email
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, phone, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create(email, password, phone, **kwargs)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    This model adds additional fields for `sso_user_id`, `email`, `national_id`, `phone`, `address`,
    and `role`, while using validators to ensure the integrity of the data.
    """

    sso_user_id = models.BigAutoField(
        unique=True,
        primary_key=True,
        db_index=True,
    )

    national_id: Optional[str] = models.CharField(
        max_length=10,
        validators=[
            UserValidator.national_id_validator,
        ],
        null=True,
        blank=True,
        db_index=True,
        verbose_name="National ID",
    )

    phone: str = models.CharField(
        max_length=11,
        validators=[
            UserValidator.phone_validator,
        ],
        null=False,
        blank=False,
        db_index=True,
        verbose_name="Phone Number",
    )

    address: Optional[str] = models.TextField(
        null=True,
        blank=True,
        verbose_name="Address",
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        validators=[
            UserValidator.email_validator,
        ],
    )

    is_email_verified = models.BooleanField(default=False)

    verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )

    verification_code_expires_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    is_banned = models.BooleanField(
        default=False,
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    class Meta:
        """
        Meta options for the User model.
        """

        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        """
        String representation of the User instance.

        Returns:
            str: Displays the user's first name, last name, and email.
        """
        return f"{self.first_name} {self.last_name} ({self.email})"

    @staticmethod
    def get_user_by_email(email: str) -> Optional["User"]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
