from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.item_factory import ItemFactory
from product.tests.factories.purchase_request_factory import PurchaseRequestFactory
from product.views.purchase_request_view import CreatePurchaseRequestAPIView, GetPurchaseRequestsForItemView, \
    GetBuyerUserPurchaseRequestView
from user.tests.factories.user_factory import UserFactory


class CreatePurchaseRequestAPITests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_purchase_for_seller_view = GetPurchaseRequestsForItemView.as_view()
        self.get_purchase_for_buyer_view = GetBuyerUserPurchaseRequestView.as_view()

        self.seller_user = UserFactory()
        self.buyer_user = UserFactory()

        self.category = CategoryFactory()
        self.item = ItemFactory(
            title="Test Item 1",
            seller_user=self.seller_user,
            category=self.category,
            price=101,
            description="Test description",
        )

        self.purchase_request = (
            PurchaseRequestFactory(item=self.item, buyer_user=self.buyer_user))

        url = reverse("get-buyer-user-purchase-request", kwargs={"item_id": self.item.id})
        self.get_buyer_purchase_request = self.factory.get(url)

        url = reverse("get-purchase-requests-for-item", kwargs={"item_id": self.item.id})
        self.get_seller_purchase_request = self.factory.get(url)

    def test_get_buyer_user_purchase_request_view_with_buyer_user(self):
        # Arrange

        force_authenticate(self.get_buyer_purchase_request, user=self.buyer_user)

        # Act
        response = self.get_purchase_for_buyer_view(
            self.get_buyer_purchase_request, item_id=self.item.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.purchase_request.id)

    def test_get_buyer_user_purchase_request_view_with_another_user(self):
        # Arrange
        force_authenticate(self.get_buyer_purchase_request, user=self.seller_user)

        # Act
        response = self.get_purchase_for_buyer_view(
            self.get_buyer_purchase_request, item_id=self.item.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, None)

    def test_get_purchase_requests_for_item_view_with_seller_user(self):
        # Arrange
        force_authenticate(self.get_seller_purchase_request, user=self.seller_user)

        # Act
        response = self.get_purchase_for_seller_view(
            self.get_seller_purchase_request, item_id=self.item.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.purchase_request.id)

    def test_get_purchase_requests_for_item_view_with_another_user_user(self):
        # Arrange

        force_authenticate(self.get_seller_purchase_request, user=self.buyer_user)

        # Act
        response = self.get_purchase_for_seller_view(
            self.get_seller_purchase_request, item_id=self.item.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item not found.")
