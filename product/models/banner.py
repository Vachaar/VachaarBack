from django.db import models

from product.models.image import Image
from product.models.item import Item
from reusable.models import BaseModel


class Banner(BaseModel):
    """
    Represents a banner, typically used for promotional or advertising purposes.

    Each banner is optionally associated with an `Item`, has an order for display sequencing,
    and includes an image file to represent the banner visually.
    """

    item: Item = models.ForeignKey(
        Item,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Associated Item",
        help_text="The item linked to this banner (if any).",
    )

    order: int = models.PositiveSmallIntegerField(
        verbose_name="Display Order",
        help_text="Determines the order in which banners are displayed. Lower values are shown first.",
    )

    image: Image = models.OneToOneField(
        Image,
        null=False,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="Banner Image",
        help_text="The image associated with this banner.",
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
        if self.item:
            return f"Banner {self.order} for Item: {self.item.title}"
        return f"Banner {self.order} (No associated item)"
