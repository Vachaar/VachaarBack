from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.models.purchase_request import PurchaseRequest
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.item_factory import ItemFactory
from product.tests.factories.purchase_request_factory import PurchaseRequestFactory
from product.views.purchase_request_view import CreatePurchaseRequestAPIView, AcceptPurchaseRequestAPIView
from user.tests.factories.user_factory import UserFactory


class AcceptPurchaseRequestViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.accept_purchase_request_view = AcceptPurchaseRequestAPIView.as_view()
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

        url = reverse("accept-purchase-request", kwargs={"purchase_request_id": self.purchase_request.id})
        self.accept_purchase_request = self.factory.post(url, {}, format="json")


    def test_accept_purchase_request_with_seller_user(self):
        # Arrange
        force_authenticate(self.accept_purchase_request, user=self.seller_user)

        # Act
        response= self.accept_purchase_request_view(
            self.accept_purchase_request, purchase_request_id=self.purchase_request.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_request.refresh_from_db()
        self.assertEqual(self.purchase_request.state, PurchaseRequest.State.ACCEPTED)

    def test_accept_purchase_request_with_another_user(self):
        # Arrange
        force_authenticate(self.accept_purchase_request, user=self.buyer_user)

        # Act
        response= self.accept_purchase_request_view(
            self.accept_purchase_request, purchase_request_id=self.purchase_request.id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], "unauthorized request.")

    def test_accept_invalid_purchase_request(self):
        # Arrange
        force_authenticate(self.accept_purchase_request, user=self.seller_user)

        # Act
        response= self.accept_purchase_request_view(
            self.accept_purchase_request, purchase_request_id=self.purchase_request.id+1)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], "purchase request not found.")

