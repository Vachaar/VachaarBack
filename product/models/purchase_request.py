from django.core.exceptions import ValidationError
from django.db import models

from product.models.item import Item
from reusable.models import BaseModel
from user.models.user import User


class PurchaseRequest(BaseModel):
    """
    Represents a request made by a user to purchase an item.
    """

    item: Item = models.ForeignKey(
        Item,
        null=False,
        blank=False,
        db_index=True,
        on_delete=models.CASCADE,
        related_query_name="purchase_requests",
        related_name="purchase_requests",
        verbose_name="Item",
    )

    buyer_user: User = models.ForeignKey(
        User,
        null=False,
        blank=False,
        db_index=True,
        on_delete=models.CASCADE,
        related_query_name="buyer",
        related_name="purchase_requests",
        verbose_name="Buyer",
    )

    comment: str = models.TextField(
        blank=True,
        verbose_name="Buyer Comment",
    )

    class State(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"

    state: str = models.CharField(
        max_length=20,
        choices=State.choices,  # type: ignore
        default=State.PENDING,
        verbose_name="Request State",
    )

    def clean(self):
        if not self.pk:
            return
        old_instance = PurchaseRequest.objects.get(pk=self.pk)

        if old_instance.state == Item.State.SOLD:
            raise ValidationError("Cannot change state of sold items.")

    class Meta:
        """
        Metadata options for the PurchaseRequest model.
        """

        verbose_name = "Purchase Request"
        verbose_name_plural = "Purchase Requests"
        ordering = ["-id"]

    def __str__(self) -> str:
        """
        String representation of the PurchaseRequest instance.

        Returns:
            str: The title of the item and the buyer user.
        """
        return f"Request for {self.item.title} by {self.buyer_user.username}"
