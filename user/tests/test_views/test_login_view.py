from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from user.models.user import User
from user.views.login_view import CustomTokenObtainPairView


class UserLoginTests(TestCase):
    def test_valid_login_credentials(self):
        # Arrange
        client = APIClient()
        url = reverse("login")
        data = {"email": "test@example.com", "password": "testpassword"}

        # Create a user with the same credentials
        User.objects.create(
            email=data["email"],
            password=data["password"],
            phone="09123456789",
            is_active=True,
        )

        # Act
        response = client.post(url, data)

        # Assert
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login_credentials(self):
        # Arrange
        client = APIClient()
        url = reverse("login")
        data = {"email": "test@example.com", "password": "wrongpassword"}

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Invalid credentials.")
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_login_throttling(self):
        # Arrange
        client = APIClient()
        url = reverse("login")
        data = {"email": "test@example.com", "password": "wrongpassword"}
        throttle_limit = 3

        # Act
        for _ in range(2):
            client.post(url, data)
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, 400)

    def test_authentication_with_valid_user(self):
        # Arrange
        user = User.objects.create(
            email="valid@example.com",
            password="testpassword",
            phone="09123456789",
        )
        request = APIClient().request()
        request.data = {
            "email": "valid@example.com",
            "password": "testpassword",
        }

        # Act
        authenticated_user = CustomTokenObtainPairView._authenticate_user(
            request
        )

        # Assert
        self.assertEqual(authenticated_user, user)

    def test_authentication_with_invalid_user(self):
        # Arrange
        request = APIClient().request()
        request.data = {
            "email": "invalid@example.com",
            "password": "wrongpassword",
        }

        # Act
        authenticated_user = CustomTokenObtainPairView._authenticate_user(
            request
        )

        # Assert
        self.assertIsNone(authenticated_user)
