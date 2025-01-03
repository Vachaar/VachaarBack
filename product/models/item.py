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

    seller_user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_query_name="seller",
        related_name="sold_items",
        verbose_name="Seller",
    )

    category_id = models.ForeignKey(
        Category,
        null=False,
        blank=False,
        default=None,
        on_delete=models.PROTECT,
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

    is_banned = models.BooleanField(
        default=False,
        verbose_name="Is Banned",
    )

    buyer_user = models.ForeignKey(
        User,
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        related_query_name="buyer",
        related_name="bought_items",
        verbose_name="buyer user",
    )

    class State(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SOLD = "sold", "Sold"
        RESERVED = "reserved", "Reserved"

    state = models.CharField(
        max_length=20,
        choices=State.choices, # type: ignore
        default=State.ACTIVE,
        verbose_name="State",
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
