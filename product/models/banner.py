from typing import Optional

from django.db import models

from product.models.item import Item
from reusable.models import BaseModel


class Banner(BaseModel):
    """
    Represents a banner, typically used for promotional or advertising purposes.

    Each banner is optionally associated with an `Item`, has an order for display sequencing,
    and includes an image file to represent the banner visually.
    """

    item_id: Optional[Item] = models.OneToOneField(
        Item,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_query_name="banner",
        related_name="banner",
        verbose_name="Associated Item",
        help_text="The item linked to this banner (if any).",
    )

    order: int = models.PositiveSmallIntegerField(
        verbose_name="Display Order",
        help_text="Determines the order in which banners are displayed. Lower values are shown first.",
    )

    image_file: models.ImageField = models.ImageField(
        upload_to="banners/",
        verbose_name="Banner Image",
        help_text="The image file for the banner.",
    )

    class Meta:
        """
        Metadata for the Banner model.
        """

        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ["-order"]

    def __str__(self) -> str:
        """
        String representation of the Banner instance.

        Returns:
            str: A string describing the banner, including its order and associated item.
        """
        if self.item_id:
            return f"Banner {self.order} for Item: {self.item_id.title}"
        return f"Banner {self.order} (No associated item)"
