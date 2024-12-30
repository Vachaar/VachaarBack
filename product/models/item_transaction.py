from typing import Optional
from django.db import models
from product.models.item import Item
from reusable.models import BaseModel
from user.models.user import User


class Transaction(BaseModel):
    """
    Represents the transaction details of an item, including its status
    and the user who reserved it (if any).
    """

    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name="transaction",
        verbose_name="Related Item",
        help_text="The item associated with this transaction.",
    )

    ACTIVE: str = "Active"
    RESERVED: str = "Reserved"
    SOLD: str = "Sold"
    BLOCKED: str = "Blocked"

    TRANSACTION_STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (RESERVED, "Reserved"),
        (SOLD, "Sold"),
        (BLOCKED, "Blocked"),
    ]

    transaction_status: str = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATUS_CHOICES,
        default=ACTIVE,
        verbose_name="Transaction Status",
        help_text="The current status of the transaction.",
    )

    reserver_user: Optional[User] = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_query_name="reserver",
        related_name="transactions",
        verbose_name="Reserver",
        help_text="The user who reserved this item (if any).",
    )

    class Meta:
        """
        Metadata options for the Transaction model.
        """

        verbose_name = "ItemTransaction"
        verbose_name_plural = "ItemTransactions"
        ordering = ["-id"]

    def __str__(self) -> str:
        """
        String representation of the Transaction instance.

        Returns:
            str: The status of the transaction.
        """
        return f"Transaction for item {self.item.title} - {self.transaction_status}"
