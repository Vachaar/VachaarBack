from typing import Optional, Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models

from user.services.validators import UserValidator


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    This model adds additional fields for `national_id`, `phone`, `address`,
    and `role`, while using validators to ensure the integrity of the data.
    """

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
    phone: Optional[str] = models.CharField(
        max_length=11,
        validators=[
            UserValidator.phone_validator,
        ],
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Phone Number",
    )
    address: Optional[str] = models.TextField(
        null=True,
        blank=True,
        verbose_name="Address",
    )

    # Role definition
    NORMAL_USER: str = "User"
    MANAGER_USER: str = "Manager"
    STAFF_USER: str = "Staff"

    ROLE_CHOICES: Tuple[Tuple[str, str], ...] = (
        (NORMAL_USER, "user"),
        (MANAGER_USER, "manager"),
        (STAFF_USER, "staff"),
    )

    role: str = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=NORMAL_USER,
        db_index=True,
        verbose_name="Role",
    )

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
