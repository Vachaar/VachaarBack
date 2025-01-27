from django.test import TestCase

from product.exceptions import (
    ImageNotFoundException,
    SellerUserIsRequiredException,
)
from product.models.banner import Banner
from product.models.item import Item
from product.services.item_repository import create_banners
from product.services.item_repository import create_item_with_banners
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.image_factory import ImageFactory
from product.tests.factories.item_factory import ItemFactory
from user.tests.factories.user_factory import UserFactory


class CreateItemWithBannersTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.image = ImageFactory()
        self.seller_user = UserFactory(
            username="test_seller", password="password"
        )
        self.item_data = {
            "title": "Test Item",
            "description": "This is a test item",
            "price": 100.00,
            "category": self.category,
            "banners": [{"image_id": self.image.id, "order": 1}],
        }

    def test_create_item_success(self):
        # Arrange
        data = self.item_data

        # Act
        item = create_item_with_banners(data, self.seller_user)

        # Assert
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, data["title"])
        self.assertEqual(item.category.id, self.category.id)
        banners = Banner.objects.filter(item=item)
        self.assertEqual(banners.count(), 1)

    def test_missing_seller_user(self):
        # Arrange
        data = self.item_data

        # Assert
        with self.assertRaises(SellerUserIsRequiredException) as context:
            # Act
            create_item_with_banners(data, None)

    def test_invalid_category(self):
        # Arrange
        data = self.item_data.copy()
        data["category"] = 99999

        # Assert
        with self.assertRaises(ValueError):
            # Act
            create_item_with_banners(data, self.seller_user)

    def test_invalid_banner_image_id(self):
        # Arrange
        data = self.item_data.copy()
        data["banners"][0]["image_id"] = 99999

        # Assert
        with self.assertRaises(ImageNotFoundException):
            # Act
            create_item_with_banners(data, self.seller_user)

    def test_atomicity_on_failure(self):
        # Arrange
        invalid_data = self.item_data.copy()
        invalid_data["banners"][0]["image_id"] = 99999

        # Act and Assert
        with self.assertRaises(ImageNotFoundException):
            create_item_with_banners(invalid_data, self.seller_user)

        # Assert
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(Banner.objects.count(), 0)

    def test_create_item_no_banners(self):
        # Arrange
        data = self.item_data.copy()
        data.pop("banners")

        # Act
        item = create_item_with_banners(data, self.seller_user)

        # Assert
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, data["title"])
        self.assertEqual(item.category.id, self.category.id)
        banners = Banner.objects.filter(item=item)
        self.assertEqual(banners.count(), 0)


class CreateBannersTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.user = UserFactory()
        self.item = ItemFactory(
            title="Test Item",
            seller_user=self.user,
            category=self.category,
            price=101,
            description="Test description",
        )
        self.image1 = ImageFactory()
        self.image2 = ImageFactory()
        self.banner_data = [
            {"image_id": self.image1.id, "order": 1},
            {"image_id": self.image2.id, "order": 2},
        ]

    def test_create_banners_success(self):
        # Arrange
        data = {"banners": self.banner_data}

        # Act
        create_banners(data, self.item)

        # Assert
        banners = Banner.objects.filter(item_id=self.item.id)
        self.assertEqual(banners.count(), 2)
        self.assertEqual(banners[0].order, 2)
        self.assertEqual(banners[1].order, 1)
        self.assertEqual(banners[0].image, self.image2)
        self.assertEqual(banners[1].image, self.image1)

    def test_create_banners_no_data(self):
        # Arrange
        data = {"banners": []}

        # Act
        create_banners(data, self.item)

        # Assert
        banners = Banner.objects.filter(item_id=self.item.id)
        self.assertEqual(banners.count(), 0)

    def test_create_banners_missing_image(self):
        # Arrange
        invalid_banner_data = [
            {"image_id": 9999, "order": 1},  # Non-existent image ID
        ]
        data = {"banners": invalid_banner_data}

        # Act & Assert
        with self.assertRaises(ImageNotFoundException):
            create_banners(data, self.item)
