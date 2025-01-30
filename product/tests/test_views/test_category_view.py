from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from product.models.category import Category
from product.tests.factories.category_factory import CategoryFactory
from product.views.category_view import CategoryListView


class CategoryListViewTests(TestCase):
    def setUp(self):
        self.view = CategoryListView.as_view()
        self.url = reverse("category-list")
        self.factory = APIRequestFactory()

    def test_get_category_list_empty(self):
        # Arrange
        Category.objects.all().delete()

        # Create the request
        request = self.factory.get(self.url)
        # Call the view directly
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_category_list_with_data(self):
        # Arrange
        Category.objects.all().delete()
        CategoryFactory(title="Category 1")
        CategoryFactory(title="Category 2")

        # Create the request
        request = self.factory.get(self.url)
        # Call the view
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Category 2")
        self.assertEqual(response.data[1]["title"], "Category 1")

    def test_endpoint_permission_allow_any(self):
        # Arrange
        CategoryFactory(title="Category 1")

        # Create the request
        request = self.factory.get(self.url)
        # Call the view
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
