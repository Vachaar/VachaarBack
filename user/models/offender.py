from typing import Optional

from django.db import models

from reusable.models import BaseModel
from user.models.user import User


class OffenderUser(BaseModel):
    """
    Represents a user who is categorized as an offender.

    This model provides a one-to-one relationship with the `User` model,
    and includes utility methods for querying offender users.
    """

    user_id: Optional[User] = models.OneToOneField(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_query_name="offender",
        related_name="offender",
        verbose_name="User",
    )

    class Meta:
        """
        Model metadata for the OffenderUser model.
        """

        unique_together = ("user_id",)
        verbose_name = "Offender User"
        verbose_name_plural = "Offender Users"

    def __str__(self) -> str:
        """
        String representation of the OffenderUser instance.

        Returns:
            str: A string describing the offender user.
        """
        return f"Offender User {self.user_id}"

    @staticmethod
    def is_user_offender(user_id: int) -> bool:
        """
        Checks if the given user ID corresponds to an offender.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is an offender, otherwise False.
        """
        return OffenderUser.objects.filter(user_id=user_id).exists()
