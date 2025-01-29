from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.models.banner import Banner
from product.models.image import Image
from product.models.item import Item
from product.tests.factories.banner_factory import BannerFactory
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.image_factory import ImageFactory
from product.tests.factories.item_factory import ItemFactory
from product.views.item_view import (
    ItemCreateView,
    ItemDetailView,
    ItemEditView,
    ItemListAllView,
    ItemDeleteView,
)
from user.tests.factories.user_factory import UserFactory


class ItemListAllViewTests(TestCase):
    def setUp(self):
        self.list_url = reverse("item-list-all")
        self.factory = APIRequestFactory()
        self.view = ItemListAllView.as_view()
        self.user = UserFactory()

        self.category = CategoryFactory()
        self.item1 = ItemFactory(
            title="Test Item 1",
            seller_user=self.user,
            category=self.category,
            price=101,
            description="Test description",
        )
        self.item2 = ItemFactory(
            title="Test Item 2",
            seller_user=self.user,
            category=self.category,
            price=110.99,
            description="Test description",
        )

    def test_list_all_items_success(self):
        # Arrange
        request = self.factory.get(self.list_url)
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]["items"]), 2)
        self.assertEqual(
            response.data["results"]["items"][0]["title"], self.item2.title
        )  # Default ordering
        self.assertEqual(
            response.data["results"]["items"][1]["title"], self.item1.title
        )

    def test_search_items_by_title(self):
        # Arrange
        request = self.factory.get(f"{self.list_url}?search=Item 1")
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]["items"]), 1)
        self.assertEqual(
            response.data["results"]["items"][0]["title"], self.item1.title
        )

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
        self.assertEqual(len(response.data["results"]["items"]), 1)
        self.assertEqual(
            response.data["results"]["items"][0]["title"], self.item1.title
        )

    def test_order_items_by_price(self):
        # Arrange
        request = self.factory.get(f"{self.list_url}?ordering=price")
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]["items"]), 2)
        self.assertEqual(
            response.data["results"]["items"][0]["title"], self.item1.title
        )
        self.assertEqual(
            response.data["results"]["items"][1]["title"], self.item2.title
        )


class TestItemCreateView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ItemCreateView.as_view()
        self.user = UserFactory()

        self.category = CategoryFactory()
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


class ItemEditViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ItemEditView.as_view()
        self.seller_user = UserFactory()
        self.another_user = UserFactory()
        self.category = CategoryFactory()
        self.some_item = ItemFactory(
            title="Test Item 0",
            seller_user=self.seller_user,
            category=self.category,
            price=101,
            description="Test description",
        )
        self.item_to_edit = ItemFactory(
            title="Test Item 1",
            seller_user=self.seller_user,
            category=self.category,
            price=101,
            description="Test description",
        )
        self.image1 = ImageFactory()
        self.image2 = ImageFactory()

        self.valid_item_id = self.item_to_edit.id
        self.invalid_item_id = 99999

        self.edit_payload = {
            "title": "Test Item 2",
            "category": self.category.id,
            "price": 50.00,
            "description": "Test Description",
            "banners": [{"image_id": self.image2.id, "order": 1}],
        }

        url = reverse("edit-item", kwargs={"item_id": self.valid_item_id})
        self.edit_valid_item_request = self.factory.put(
            url, data=self.edit_payload, format="json"
        )

    def test_edit_valid_item(self):
        # Arrange
        force_authenticate(self.edit_valid_item_request, user=self.seller_user)

        # Act
        response = self.view(self.edit_valid_item_request, self.valid_item_id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item_to_edit.refresh_from_db()
        self.assertEqual(self.item_to_edit.title, "Test Item 2")
        banners = Banner.objects.all()
        self.assertEqual(len(banners), 1)
        banner = banners[0]
        self.assertEqual(banner.image.id, self.image2.id)

    def test_edit_item_unauthenticated(self):
        # Arrange
        force_authenticate(self.edit_valid_item_request, user=self.another_user)

        # Act
        response = self.view(self.edit_valid_item_request, self.valid_item_id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "unauthorized request.")

    def test_edit_invalid_item(self):
        # Arrange
        url = reverse("edit-item", kwargs={"item_id": self.invalid_item_id})
        request = self.factory.put(url, data=self.edit_payload, format="json")
        force_authenticate(request, user=self.seller_user)

        # Act
        response = self.view(request, self.invalid_item_id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item not found.")


class ItemDeleteViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ItemDeleteView.as_view()
        self.seller_user = UserFactory()
        self.another_user = UserFactory()

        self.invalid_item_id = 9999

        self.category = CategoryFactory()
        self.item_to_delete = ItemFactory(
            title="Test Item 0",
            seller_user=self.seller_user,
            category=self.category,
            price=101,
            description="Test description",
        )
        self.some_item = ItemFactory(
            title="Test Item 1",
            seller_user=self.seller_user,
            category=self.category,
            price=101,
            description="Test description",
        )

        self.image1 = ImageFactory()
        self.banner1 = BannerFactory(
            item=self.item_to_delete, image=self.image1, order=1
        )

        self.image2 = ImageFactory()
        self.banner2 = BannerFactory(
            item=self.some_item, image=self.image2, order=1
        )

        url = reverse("delete-item", kwargs={"item_id": self.item_to_delete.id})
        self.delete_valid_item_request = self.factory.delete(url, format="json")

    def test_delete_valid_item(self):
        # Arrange
        force_authenticate(
            self.delete_valid_item_request, user=self.seller_user
        )

        # Act
        response = self.view(
            self.delete_valid_item_request, self.item_to_delete.id
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(Item.objects.all()), 1)
        self.assertEqual(len(Banner.objects.all()), 1)
        self.assertEqual(len(Image.objects.all()), 1)

        self.assertEqual(Item.objects.first().id, self.some_item.id)
        self.assertEqual(Banner.objects.first().id, self.banner2.id)
        self.assertEqual(Image.objects.first().id, self.image2.id)

    def test_delete_item_unauthenticated(self):
        # Arrange
        force_authenticate(
            self.delete_valid_item_request, user=self.another_user
        )

        # Act
        response = self.view(
            self.delete_valid_item_request, self.item_to_delete.id
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "unauthorized request.")

    def test_delete_invalid_item(self):
        # Arrange
        url = reverse("delete-item", kwargs={"item_id": self.invalid_item_id})
        request = self.factory.delete(url, format="json")
        force_authenticate(request, user=self.seller_user)

        # Act
        response = self.view(request, self.invalid_item_id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item not found.")


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
            price=101,
            description="Test description",
        )
        self.valid_item_id = self.item.id
        self.invalid_item_id = 99999

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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
