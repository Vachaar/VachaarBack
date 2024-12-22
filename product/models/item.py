from typing import Optional

from django.db import models

from product.models.category import Category
from reusable.models import AmountField, BaseModel
from user.models.user import User


class Item(BaseModel):
    """
    Represents an item in the inventory with details such as title, category, price,
    description, transaction status, seller, and reserver.
    """

    title: str = models.CharField(
        max_length=255,
        verbose_name="Item Title",
    )

    category_id: Optional[Category] = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_query_name="category",
        related_name="items",
        verbose_name="Category",
    )

    price: Optional[AmountField] = AmountField(
        verbose_name="Price",
    )

    description: Optional[str] = models.TextField(
        blank=True,
        verbose_name="Item Description",
    )

    # Transaction status choices
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
    )

    seller_user: Optional[User] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_query_name="seller",
        related_name="sold_items",
        verbose_name="Seller",
    )

    reserver_user: Optional[User] = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_query_name="reserver",
        related_name="reserved_items",
        verbose_name="Reserver",
    )

    class Meta:
        """
        Metadata options for the Item model.
        """

        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["-id"]

    def __str__(self) -> str:
        """
        String representation of the Item instance.

        Returns:
            str: The title of the item.
        """
        return self.title
