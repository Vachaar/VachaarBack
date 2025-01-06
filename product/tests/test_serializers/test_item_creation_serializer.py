from django.test import TestCase
from rest_framework.exceptions import ValidationError

from product.serializers.item_creation_serializer import ItemCreationSerializer
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.image_factory import ImageFactory


class ItemCreationSerializerTests(TestCase):
    def setUp(self):
        self.valid_category = CategoryFactory()
        self.valid_image = ImageFactory()
        self.valid_data = {
            "title": "Sample Item",
            "category": self.valid_category.id,
            "price": 19.99,
            "description": "Sample description",
            "banners": [{"image_id": self.valid_image.id, "order": 1}],
        }

    def test_serializer_valid_data(self):
        serializer = ItemCreationSerializer(data=self.valid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_serializer_missing_title(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("title")
        serializer = ItemCreationSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_missing_category(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("category")
        serializer = ItemCreationSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_missing_price(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("price")
        serializer = ItemCreationSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_invalid_category(self):
        invalid_data = self.valid_data.copy()
        invalid_data["category"] = 9999
        serializer = ItemCreationSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_serializer_invalid_price(self):
        invalid_data = self.valid_data.copy()
        invalid_data["price"] = "invalid_price"
        serializer = ItemCreationSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_missing_banners(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("banners")
        serializer = ItemCreationSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_serializer_invalid_banners(self):
        invalid_data = self.valid_data.copy()
        invalid_data["banners"] = [{"image_id": 9999, "order": 1}]
        serializer = ItemCreationSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_empty_description(self):
        valid_data = self.valid_data.copy()
        valid_data["description"] = ""
        serializer = ItemCreationSerializer(data=valid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
