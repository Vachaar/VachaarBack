from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from product.models.category import Category
from product.tests.factories.category_factory import CategoryFactory


class CategoryListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_category_list_empty(self):
        # Arrange
        Category.objects.all().delete()

        # Act
        response = self.client.get(reverse("category-list"))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_get_category_list_with_data(self):
        # Arrange
        Category.objects.all().delete()

        CategoryFactory(title="Category 1")
        CategoryFactory(title="Category 2")

        # Act
        response = self.client.get(reverse("category-list"))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["title"], "Category 2")
        self.assertEqual(response.json()[1]["title"], "Category 1")

    def test_endpoint_permission_allow_any(self):
        # Arrange
        CategoryFactory(title="Category 1")
        url = reverse("category-list")

        # Act
        response_unauthenticated = self.client.get(url)

        # Assert
        self.assertEqual(
            response_unauthenticated.status_code, status.HTTP_200_OK
        )
