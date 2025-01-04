from django.test import TestCase
from rest_framework.exceptions import ValidationError

from product.serializers.category_serializer import CategorySerializer
from product.tests.factories.category_factory import CategoryFactory


class CategorySerializerTests(TestCase):
    def setUp(self):
        self.valid_category_data = {
            "title": "Electronics",
        }
        self.invalid_category_data = {
            "title": "",
        }
        self.category = CategoryFactory(title="Books")

    def test_serializer_valid_data(self):
        # Arrange
        serializer = CategorySerializer(data=self.valid_category_data)
        # Act
        is_valid = serializer.is_valid()
        # Assert
        self.assertTrue(is_valid)

    def test_serializer_invalid_data(self):
        # Arrange
        serializer = CategorySerializer(data=self.invalid_category_data)
        # Act & Assert
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_serializer_saves_valid_data(self):
        # Arrange
        serializer = CategorySerializer(data=self.valid_category_data)
        # Act
        serializer.is_valid()
        category = serializer.save()
        # Assert
        self.assertEqual(category.title, self.valid_category_data["title"])

    def test_serializer_returns_expected_fields(self):
        # Arrange
        serializer = CategorySerializer(instance=self.category)
        # Act
        data = serializer.data
        # Assert
        self.assertIn("title", data)
        self.assertEqual(data["title"], self.category.title)

    def test_serializer_rejects_empty_data(self):
        # Arrange
        serializer = CategorySerializer(data={})
        # Act & Assert
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
