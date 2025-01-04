from django.test import TestCase
from rest_framework.exceptions import ValidationError

from product.serializers.banner_data_serializer import BannerDataSerializer
from product.tests.factories.image_factory import ImageFactory


class BannerDataSerializerTests(TestCase):
    def setUp(self):
        self.valid_image_id = 1
        self.invalid_image_id = 999  # Non-existent image_id
        self.valid_order = 1
        self.invalid_order = -5

        # Create a sample image in the database
        ImageFactory(id=self.valid_image_id)

    def test_serializer_valid_data(self):
        # Arrange
        valid_data = {
            "image_id": self.valid_image_id,
            "order": self.valid_order,
        }

        # Act
        serializer = BannerDataSerializer(data=valid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertTrue(is_valid)

    def test_serializer_invalid_image_id(self):
        # Arrange
        invalid_data = {
            "image_id": self.invalid_image_id,
            "order": self.valid_order,
        }

        # Act
        serializer = BannerDataSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_serializer_invalid_order_value(self):
        # Arrange
        invalid_data = {
            "image_id": self.valid_image_id,
            "order": self.invalid_order,
        }

        # Act
        serializer = BannerDataSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_serializer_missing_image_id(self):
        # Arrange
        invalid_data = {"order": self.valid_order}

        # Act
        serializer = BannerDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)

    def test_serializer_missing_order(self):
        # Arrange
        invalid_data = {"image_id": self.valid_image_id}

        # Act
        serializer = BannerDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)

    def test_serializer_order_is_zero(self):
        # Arrange
        invalid_data = {"image_id": self.valid_image_id, "order": 0}

        # Act
        serializer = BannerDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
