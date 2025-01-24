from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.models.purchase_request import PurchaseRequest
from product.tests.factories.category_factory import CategoryFactory
from product.tests.factories.item_factory import ItemFactory
from product.views.purchase_request_view import CreatePurchaseRequestAPIView
from user.tests.factories.user_factory import UserFactory


class CreatePurchaseRequestAPITests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.create_view = CreatePurchaseRequestAPIView.as_view()
        self.buyer_user = UserFactory()
        self.seller_user = UserFactory()

        self.category = CategoryFactory()
        self.item = ItemFactory(
            title="Test Item 1",
            seller_user=self.seller_user,
            category=self.category,
            price=101,
            description="Test description",
        )

        self.create_url = reverse("create-purchase-request")

    def test_create_purchase_with_existing_item(self):
        # Arrange
        data = {
            "item_id": self.item.id,
            "comment": "I want to buy this item."
        }

        request = self.factory.post(self.create_url, data, format='json')
        force_authenticate(request, user=self.buyer_user)

        # Act
        response = self.create_view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        request_id = response.data["request_id"]
        self.assertTrue(PurchaseRequest.objects.filter(id=request_id).exists())

    def test_create_purchase_with_non_existing_item(self):
        # Arrange
        data = {
            "item_id": self.item.id + 1,
            "comment": "I want to buy this item."
        }

        request = self.factory.post(self.create_url, data, format='json')
        force_authenticate(request, user=self.buyer_user)  # Authenticate as buyer user

        # Act
        response = self.create_view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "item not found.")
