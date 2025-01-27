from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.models.banner import Banner
from product.tests.factories.banner_factory import BannerFactory
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.image_factory import ImageFactory
from product.tests.factories.item_factory import ItemFactory
from product.views.item_view import ItemListView, ItemCreateView, ItemDetailView, ItemEditView
from user.tests.factories.user_factory import UserFactory


class ItemListAllViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ItemListView.as_view()
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
        self.category1 = CategoryFactory()
        self.category2 = CategoryFactory()
        self.item0 = ItemFactory(
            title="Test Item 0",
            seller_user=self.seller_user,
            category=self.category1,
            price=101,
            description="Test description"
        )
        self.item1 = ItemFactory(
            title="Test Item 1",
            seller_user=self.seller_user,
            category=self.category1,
            price=101,
            description="Test description"
        )
        self.image1 = ImageFactory()
        self.banner1 = BannerFactory(item=self.item1, image=self.image1, order=1)

        self.valid_item_id = self.item1.id
        self.invalid_item_id = 99999

        self.image2 = ImageFactory()
        self.edit_payload = {
            "title": "Test Item 2",
            "category": self.category1.id,
            "price": 50.00,
            "description": "Test Description",
            "banners": [{"image_id": self.image2.id, "order": 1}],
        }
        url = reverse("edit-item", kwargs={"item_id": self.valid_item_id})
        self.edit_valid_item_request = self.factory.put(url, data=self.edit_payload, format="json")

    def test_edit_valid_item(self):
        # Arrange
        force_authenticate(self.edit_valid_item_request, user=self.seller_user)

        # Act
        response = self.view(self.edit_valid_item_request, self.valid_item_id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.title, "Test Item 2")
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
