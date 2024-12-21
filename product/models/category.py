from django.db import models

from reusable.models import BaseModel


class Category(BaseModel):
    """
    Represents a category that can be used to group related items.

    This model includes a title field to specify the category name.
    """

    title: str = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Category Title",
        help_text="The name of the category.",
    )

    class Meta:
        """
        Metadata options for the Category model.
        """

        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-id"]

    def __str__(self) -> str:
        """
        String representation of the Category instance.

        Returns:
            str: The title of the category.
        """
        return self.title
