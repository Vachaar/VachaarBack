from django.db import models

from reusable.models import BaseModel


class Image(BaseModel):
    """
    Model to store image files directly in the database.
    """
    content_type = models.CharField(
        max_length=50,
        verbose_name="Content Type",
        help_text="The MIME type of the image file (e.g., image/jpeg).",
    )
    image_data = models.BinaryField(
        verbose_name="Image Data",
        help_text="The binary data of the image file.",
    )

    def __str__(self):
        return f"Image ID: {self.id}"
