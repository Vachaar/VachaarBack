from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models.user import User
from user.tests.factories.user_factory import UserFactory
from user.views.register_view import RegisterView


class UserRegistrationTests(TestCase):
    def test_create_user_success(self):
        # Arrange
        client = APIClient()
        url = reverse(
            "register"
        )  # Adjust the URL name as per your route configuration
        data = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "phone": "09123456789",
        }

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()["detail"],
            RegisterView.SUCCESS_MESSAGE.get("detail"),
        )
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_create_user_missing_email(self):
        # Arrange
        client = APIClient()
        url = reverse("register")
        data = {"password": "securepassword123", "name": "Test User"}

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.json())

    def test_create_user_email_already_exists(self):
        # Arrange
        client = APIClient()
        url = reverse("register")
        existing_email = "testuser@example.com"
        password = "securepassword123"
        phone = "09123456789"
        UserFactory(email=existing_email, password=password, phone=phone)
        data = {
            "email": existing_email,
            "password": "newsecurepassword123",
            "phone": phone,
        }

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_throttling(self):
        # Arrange
        client = APIClient()
        url = reverse("register")
        data = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "name": "Test User",
        }

        # Act
        for _ in range(
            5
        ):  # Simulate multiple requests exceeding throttle limit
            client.post(url, data)
        response = client.post(url, data)

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_429_TOO_MANY_REQUESTS
        )  # Too many requests

    def test_create_user_invalid_email_format(self):
        # Arrange
        client = APIClient()
        url = reverse("register")
        data = {
            "email": "invalidemail",
            "password": "securepassword123",
            "name": "Test User",
        }

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.json())
