from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from user.exceptions import InvalidCredentialsException
from user.tests.factories.user_factory import UserFactory
from user.views.login_view import CustomTokenObtainPairView


class UserLoginTests(TestCase):
    def test_valid_login_credentials(self):
        # Arrange
        client = APIClient()
        url = reverse("login")
        data = {"email": "test@example.com", "password": "testpassword"}

        # Create a user with the same credentials
        UserFactory(
            email=data["email"],
            password=data["password"],
        )

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["detail"],
            CustomTokenObtainPairView.LOGIN_SUCCESS_MSG["detail"],
        )
        self.assertIn("access", response.cookies)
        self.assertIn("refresh", response.cookies)

    def test_invalid_login_credentials(self):
        # Arrange
        client = APIClient()
        url = reverse("login")
        data = {"email": "test@example.com", "password": "wrongpassword"}

        # Act
        response = client.post(url, data)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["message"], InvalidCredentialsException.default_detail
        )
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
        email = "valid@example.com"
        password = "testpassword"
        user = UserFactory(email=email, password=password)

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
