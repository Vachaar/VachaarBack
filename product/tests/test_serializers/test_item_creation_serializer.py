from django.test import TestCase

from product.exceptions import CategoryDoesNotExistException
from product.serializers.item_data_serializer import ItemDataSerializer
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.image_factory import ImageFactory


class ItemCreationSerializerTests(TestCase):
    def setUp(self):
        self.valid_category = CategoryFactory()
        self.valid_image = ImageFactory()
        self.valid_data = {
            "title": "Sample Item",
            "category": self.valid_category.id,
            "price": 20,
            "description": "Sample description",
            "banners": [{"image_id": self.valid_image.id, "order": 1}],
        }

    def test_serializer_valid_data(self):
        serializer = ItemDataSerializer(data=self.valid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_serializer_missing_title(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("title")
        serializer = ItemDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_missing_category(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("category")
        serializer = ItemDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_missing_price(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("price")
        serializer = ItemDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_invalid_category(self):
        invalid_data = self.valid_data.copy()
        invalid_data["category"] = 9999
        serializer = ItemDataSerializer(data=invalid_data)
        with self.assertRaises(CategoryDoesNotExistException):
            serializer.is_valid(raise_exception=True)

    def test_serializer_invalid_price(self):
        invalid_data = self.valid_data.copy()
        invalid_data["price"] = "invalid_price"
        serializer = ItemDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_missing_banners(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("banners")
        serializer = ItemDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_serializer_invalid_banners(self):
        invalid_data = self.valid_data.copy()
        invalid_data["banners"] = [{"image_id": 9999, "order": 1}]
        serializer = ItemDataSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_empty_description(self):
        valid_data = self.valid_data.copy()
        valid_data["description"] = ""
        serializer = ItemDataSerializer(data=valid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
