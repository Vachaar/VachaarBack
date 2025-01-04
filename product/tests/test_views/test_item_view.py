from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.image_factory import ImageFactory
from product.tests.factories.item_factory import ItemFactory
from product.views.item_view import ItemListView, ItemCreateView, ItemDetailView
from user.tests.factories.user_factory import UserFactory


class ItemListAllViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ItemListView.as_view()
        self.user = UserFactory()

        self.category = CategoryFactory(title="Test Category")
        self.item1 = ItemFactory(
            title="Test Item 1",
            seller_user=self.user,
            category=self.category,
            price=100.99,
            description="Test description",
        )
        self.item2 = ItemFactory(
            title="Test Item 2",
            seller_user=self.user,
            category=self.category,
            price=110.99,
            description="Test description",
        )

        self.list_url = reverse("profile-item-list")

    def test_list_all_items_success(self):
        # Arrange
        request = self.factory.get(self.list_url)
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0]["title"], self.item2.title
        )  # Default ordering
        self.assertEqual(response.data["results"][1]["title"], self.item1.title)

    def test_search_items_by_title(self):
        # Arrange
        request = self.factory.get(f"{self.list_url}?search=Item 1")
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], self.item1.title)

    def test_filter_items_by_category(self):
        # Arrange
        request = self.factory.get(
            f"{self.list_url}?category_id={self.category.id}"
        )
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_items_by_price_range(self):
        # Arrange
        request = self.factory.get(
            f"{self.list_url}?price__gte=100&price__lte=105"
        )
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], self.item1.title)

    def test_order_items_by_price(self):
        # Arrange
        request = self.factory.get(f"{self.list_url}?ordering=price")
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], self.item1.title)
        self.assertEqual(response.data["results"][1]["title"], self.item2.title)


class TestItemCreateView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ItemCreateView.as_view()
        self.user = UserFactory()

        self.category = CategoryFactory(title="Test Category")
        self.image = ImageFactory()

        self.valid_payload = {
            "title": "Test Item",
            "category": self.category.id,
            "price": 50.00,
            "description": "Test Description",
            "banners": [{"image_id": self.image.id, "order": 1}],
        }
        self.invalid_payload = {
            "title": "",
            "category": 999,
            "price": "invalid_price",
            "banners": [],
        }
        self.create_url = reverse("create-item")

    def test_create_item_with_valid_payload(self):
        # Arrange
        request = self.factory.post(
            self.create_url, data=self.valid_payload, format="json"
        )
        force_authenticate(request, user=self.user)
        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("item_id", response.data)

    def test_create_item_with_invalid_payload(self):
        # Arrange
        request = self.factory.post(
            self.create_url, data=self.invalid_payload, format="json"
        )
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ItemDetailViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ItemDetailView.as_view()
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.item = ItemFactory(
            title="Test Item",
            seller_user=self.user,
            category=self.category,
            price=100.99,
            description="Test description",
        )
        self.valid_item_id = self.item.id
        self.invalid_item_id = 99999

    def test_retrieve_item_unauthenticated(self):
        # Arrange
        request = self.factory.get(
            reverse("item-detail", kwargs={"item_id": self.valid_item_id})
        )
        # Act
        response = self.view(request)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_item_authenticated(self):
        # Arrange
        request = self.factory.get(
            reverse("item-detail", kwargs={"item_id": self.valid_item_id})
        )
        force_authenticate(request, user=self.user)
        # Act
        response = self.view(request, item_id=self.valid_item_id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.valid_item_id)

    def test_get_item_not_found(self):
        # Arrange
        request = self.factory.get(
            reverse("item-detail", kwargs={"item_id": self.invalid_item_id})
        )
        force_authenticate(request, user=self.user)
        # Act
        response = self.view(request, item_id=self.invalid_item_id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
