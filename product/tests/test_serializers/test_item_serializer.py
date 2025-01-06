from django.test import TestCase

from product.serializers.item_serializer import ItemWithImagesSerializer
from product.tests.factories.banner_factory import BannerFactory
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.image_factory import ImageFactory
from product.tests.factories.item_factory import ItemFactory
from user.tests.factories.user_factory import UserFactory


class ItemWithImagesSerializerTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.user = UserFactory()
        self.item = ItemFactory(
            title="Test Item",
            seller_user=self.user,
            category=self.category,
            price=100,
            description="Test description",
        )
        self.image1 = ImageFactory()
        self.image2 = ImageFactory()
        self.banner1 = BannerFactory(item=self.item, image=self.image1, order=1)
        self.banner2 = BannerFactory(item=self.item, image=self.image2, order=2)

    def test_serializer_fields(self):
        # Arrange
        serializer = ItemWithImagesSerializer(instance=self.item)
        # Act
        data = serializer.data
        # Assert
        self.assertIn("id", data)
        self.assertIn("title", data)
        self.assertIn("category", data)
        self.assertIn("price", data)
        self.assertIn("description", data)
        self.assertIn("image_ids", data)

    def test_serializer_image_ids(self):
        # Arrange
        serializer = ItemWithImagesSerializer(instance=self.item)
        # Act
        data = serializer.data
        # Assert
        self.assertListEqual(
            list(data["image_ids"]), [self.image1.id, self.image2.id]
        )

    def test_serializer_empty_image_ids(self):
        # Arrange
        item_without_banners = ItemFactory(
            title="New Test Item",
            seller_user=self.user,
            category=self.category,
            price=150,
            description="Another test description",
        )
        serializer = ItemWithImagesSerializer(instance=item_without_banners)
        # Act
        data = serializer.data
        # Assert
        self.assertListEqual(list(data["image_ids"]), [])

    def test_serializer_valid_data(self):
        # Arrange
        serializer = ItemWithImagesSerializer(instance=self.item)
        # Act
        serialized_data = serializer.data
        # Assert
        self.assertIn("title", serialized_data)
        self.assertEqual(serialized_data["title"], self.item.title)
        self.assertIn("category", serialized_data)
        self.assertEqual(serialized_data["category"], self.item.category.id)
        self.assertIn("price", serialized_data)

        self.assertEqual(
            round(float(serialized_data["price"]), 2), round(self.item.price, 2)
        )

        self.assertIn("description", serialized_data)
        self.assertEqual(serialized_data["description"], self.item.description)
        self.assertIn("image_ids", serialized_data)
