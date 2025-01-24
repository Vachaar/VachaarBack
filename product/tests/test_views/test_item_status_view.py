from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.models.item import Item
from product.models.purchase_request import PurchaseRequest
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.item_factory import ItemFactory
from product.tests.factories.purchase_request_factory import PurchaseRequestFactory
from product.views.item_status_view import MarkItemAsSoldAPIView, ReactivateItemAPIView
from user.tests.factories.user_factory import UserFactory


class MarkItemAsSoldViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.mark_as_sold_view = MarkItemAsSoldAPIView.as_view()
        self.seller_user = UserFactory()
        self.buyer_user = UserFactory()
        category = CategoryFactory()
        self.reserved_item = ItemFactory(
            title="Reserved Item",
            seller_user=self.seller_user,
            category=category,
            price=101,
            description="Test description",
            state=Item.State.RESERVED,
        )
        self.active_item = ItemFactory(
            title="Active Item",
            seller_user=self.seller_user,
            category=category,
            price=101,
            description="Test description",
            state=Item.State.ACTIVE,
        )

        url = reverse("mark_item_as_sold", kwargs={"item_id": self.reserved_item.id})
        self.mark_reserved_item_as_sold_request = self.factory.post(url)

        url = reverse("mark_item_as_sold", kwargs={"item_id": self.active_item.id})
        self.mark_active_item_as_sold_request = self.factory.post(url)

    def test_mark_item_as_sold_successfully(self):
        # Arrange
        force_authenticate(self.mark_reserved_item_as_sold_request, user=self.seller_user)

        # Act
        response = self.mark_as_sold_view(
            self.mark_reserved_item_as_sold_request, item_id=self.reserved_item.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reserved_item.refresh_from_db()
        self.assertEqual(self.reserved_item.state, Item.State.SOLD)

    def test_mark_active_item_as_sold(self):
        # Arrange
        force_authenticate(self.mark_active_item_as_sold_request, user=self.seller_user)

        # Act
        response = self.mark_as_sold_view(
            self.mark_active_item_as_sold_request, item_id=self.active_item.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item was not reserved.")

    def test_mark_item_as_sold_unauthorized_user(self):
        # Arrange
        force_authenticate(self.mark_reserved_item_as_sold_request, user=self.buyer_user)

        # Act
        response = self.mark_as_sold_view(
            self.mark_reserved_item_as_sold_request, item_id=self.reserved_item.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "unauthorized request.")

    def test_mark_invalid_item_as_sold(self):
        # Arrange
        force_authenticate(self.mark_reserved_item_as_sold_request, user=self.seller_user)

        # Act
        response = self.mark_as_sold_view(
            self.mark_reserved_item_as_sold_request,
            item_id=self.reserved_item.id + self.active_item.id + 1)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item not found.")


class ReactivateItemViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.reactivate_item_view = ReactivateItemAPIView.as_view()
        self.seller_user = UserFactory()
        self.buyer_user = UserFactory()
        category = CategoryFactory()

        self.reserved_item = ItemFactory(
            title="Reserved Item",
            seller_user=self.seller_user,
            category=category,
            price=101,
            description="Test description",
            state=Item.State.RESERVED,
        )
        self.purchase_request = PurchaseRequestFactory(
            item=self.reserved_item,
            buyer_user=self.buyer_user,
            state=PurchaseRequest.State.ACCEPTED,
        )

        self.active_item = ItemFactory(
            title="Active Item",
            seller_user=self.seller_user,
            category=category,
            price=101,
            description="Test description",
            state=Item.State.ACTIVE,
        )

        reactivate_reserved_item_url = reverse("reactivate_item",
                                               kwargs={"item_id": self.reserved_item.id})
        self.reactivate_reserved_item_request = self.factory.post(reactivate_reserved_item_url)

        # URL for active item
        reactivate_active_item_url = reverse("reactivate_item",
                                             kwargs={"item_id": self.active_item.id})
        self.reactivate_active_item_request = self.factory.post(reactivate_active_item_url)

    def test_reactivate_reserved_item_successfully(self):
        # Arrange
        force_authenticate(self.reactivate_reserved_item_request, user=self.seller_user)

        # Act
        response = self.reactivate_item_view(
            self.reactivate_reserved_item_request, item_id=self.reserved_item.id
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.reserved_item.refresh_from_db()
        self.assertEqual(self.reserved_item.state, Item.State.ACTIVE)

        self.purchase_request.refresh_from_db()
        self.assertEqual(self.purchase_request.state, PurchaseRequest.State.PENDING)

    def test_reactivate_active_item(self):
        # Arrange
        force_authenticate(self.reactivate_active_item_request, user=self.seller_user)

        # Act
        response = self.reactivate_item_view(
            self.reactivate_active_item_request, item_id=self.active_item.id
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item was not reserved.")

    def test_reactivate_item_unauthorized_user(self):
        # Arrange
        force_authenticate(self.reactivate_reserved_item_request, user=self.buyer_user)

        # Act
        response = self.reactivate_item_view(
            self.reactivate_reserved_item_request, item_id=self.reserved_item.id
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "unauthorized request.")

    def test_reactivate_nonexistent_item(self):
        # Arrange
        non_existent_item_id = self.reserved_item.id + self.active_item.id + 1
        url = reverse("reactivate_item", kwargs={"item_id": non_existent_item_id})
        request = self.factory.post(url)
        force_authenticate(request, user=self.seller_user)

        # Act
        response = self.reactivate_item_view(request, item_id=non_existent_item_id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item not found.")
