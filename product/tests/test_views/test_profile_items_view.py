from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.models.item import Item
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.item_factory import ItemFactory
from product.views.profile_items_view import ProfileItemsAPIView
from user.tests.factories.user_factory import UserFactory


class ProfileItemsAPIViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileItemsAPIView.as_view()

        self.seller_user = UserFactory()
        self.buyer_user = UserFactory()
        self.category = CategoryFactory()

        self.reserved_item = ItemFactory(
            title="Reserved Item",
            seller_user=self.seller_user,
            buyer_user=self.buyer_user,
            category=self.category,
            price=101,
            description="This item is reserved.",
            state=Item.State.RESERVED,
        )
        self.sold_item = ItemFactory(
            title="Sold Item",
            seller_user=self.seller_user,
            buyer_user=self.buyer_user,
            category=self.category,
            price=99,
            description="This item has been sold.",
            state=Item.State.SOLD,
        )
        self.active_item = ItemFactory(
            title="Active Item",
            seller_user=self.seller_user,
            category=self.category,
            price=150,
            description="This item is active for sale.",
            state=Item.State.ACTIVE,
        )
        self.inactive_item = ItemFactory(
            title="Seller's Reserved Item",
            seller_user=self.seller_user,
            category=self.category,
            price=120,
            description="This item is inactive.",
            state=Item.State.INACTIVE,
        )

    def test_filter_reserved_by_user(self):
        # Arrange
        url = reverse(
            "profile-item-list", kwargs={"filter_group": "reserved_by_user"}
        )
        request = self.factory.get(url)
        force_authenticate(request, user=self.buyer_user)

        # Act
        response = self.view(request, filter_group="reserved_by_user")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.reserved_item.id)

    def test_filter_bought_by_user(self):
        # Arrange
        url = reverse(
            "profile-item-list", kwargs={"filter_group": "bought_by_user"}
        )
        request = self.factory.get(url)
        force_authenticate(request, user=self.buyer_user)

        # Act
        response = self.view(request, filter_group="bought_by_user")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.sold_item.id)

    def test_filter_sold_by_user(self):
        # Arrange
        url = reverse(
            "profile-item-list", kwargs={"filter_group": "sold_by_user"}
        )
        request = self.factory.get(url)
        force_authenticate(request, user=self.seller_user)

        # Act
        response = self.view(request, filter_group="sold_by_user")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.sold_item.id)

    def test_filter_created_by_user_active(self):
        # Arrange
        url = reverse(
            "profile-item-list",
            kwargs={"filter_group": "created_by_user_active"},
        )
        request = self.factory.get(url)
        force_authenticate(request, user=self.seller_user)

        # Act
        response = self.view(request, filter_group="created_by_user_active")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.active_item.id)

    def test_filter_created_by_user_reserved(self):
        # Arrange
        url = reverse(
            "profile-item-list",
            kwargs={"filter_group": "created_by_user_reserved"},
        )
        request = self.factory.get(url)
        force_authenticate(request, user=self.seller_user)

        # Act
        response = self.view(request, filter_group="created_by_user_reserved")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.reserved_item.id)

    def test_invalid_filter_group(self):
        # Arrange
        url = reverse(
            "profile-item-list", kwargs={"filter_group": "invalid_filter"}
        )
        request = self.factory.get(url)
        force_authenticate(request, user=self.buyer_user)

        # Act
        response = self.view(request, filter_group="invalid_filter")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "invalid filter group.")
