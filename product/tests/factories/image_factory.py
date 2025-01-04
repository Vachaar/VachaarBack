from io import BytesIO

import factory
from PIL import Image as PILImage

from product.models.image import Image


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    content_type = factory.Faker("mime_type", category="image")

    @factory.lazy_attribute
    def image_data(self):
        img = PILImage.new("RGB", (100, 100), color=(255, 0, 0))
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        return buffer.getvalue()
