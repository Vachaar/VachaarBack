from typing import Optional

from django.db import models

from product.models.item import Item
from reusable.models import BaseModel
from user.models.user import User


class Violation(BaseModel):
    """
    Represents a violation report in the system.

    A violation is associated with an item, reported by a user,
    and includes a description along with its current status
    (e.g., Approved, Rejected, Under Review).
    """

    item: Optional[Item] = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="violations",
        verbose_name="Reported Item",
        help_text="The item associated with this violation.",
    )

    description: Optional[str] = models.TextField(
        verbose_name="Violation Description",
        help_text="Details about the reported violation.",
    )

    reporter_user: Optional[User] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reported_violations",
        verbose_name="Reporter User",
        help_text="The user who reported this violation.",
    )

    APPROVED: str = "Approved"
    REJECTED: str = "Rejected"
    UNDER_REVIEW: str = "Under Review"

    STATUS_CHOICES = [
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (UNDER_REVIEW, "Under Review"),
    ]

    status: str = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=UNDER_REVIEW,
        verbose_name="Violation Status",
        help_text="The current status of the violation.",
    )

    class Meta:
        """
        Metadata for the Violation model.
        """

        verbose_name = "Violation"
        verbose_name_plural = "Violations"
        ordering = ["-id"]  # Order by most recently created violations

    def __str__(self) -> str:
        """
        String representation of the Violation instance.

        Returns:
            str: A string describing the violation's ID and status.
        """
        return f"Violation {self.id} - {self.status}"
