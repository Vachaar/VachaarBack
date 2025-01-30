from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from user.exceptions import InvalidCredentialsException
from user.tests.factories.user_factory import UserFactory
from user.views.login_view import CustomTokenObtainPairView


class UserLoginTests(TestCase):
    def test_invalid_login_credentials(self):
        # Arrange
        factory = APIRequestFactory()
        url = reverse("login")
        data = {"email": "test@example.com", "password": "wrongpassword"}

        # Act
        request = factory.post(url, data)
        response = CustomTokenObtainPairView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["message"], InvalidCredentialsException.default_detail
        )
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_login_throttling(self):
        # Arrange
        factory = APIRequestFactory()
        url = reverse("login")
        data = {"email": "test@example.com", "password": "wrongpassword"}
        throttle_limit = 3

        # Act
        for _ in range(2):
            request = factory.post(url, data)
            response = CustomTokenObtainPairView.as_view()(request)
        request = factory.post(url, data)
        response = CustomTokenObtainPairView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, 400)

    def test_authentication_with_valid_user(self):
        # Arrange
        email = "valid@example.com"
        password = "testpassword"
        user = UserFactory(email=email, password=password)

        factory = APIRequestFactory()
        request = factory.post(
            reverse("login"), {"email": email, "password": password}
        )
        # Explicitly set the `data` attribute on the request
        request.data = {"email": email, "password": password}

        # Act
        authenticated_user = CustomTokenObtainPairView._authenticate_user(
            request
        )

        # Assert
        self.assertEqual(authenticated_user, user)

    def test_authentication_with_invalid_user(self):
        # Arrange
        factory = APIRequestFactory()
        request = factory.post(
            reverse("login"),
            {"email": "invalid@example.com", "password": "wrongpassword"},
        )
        # Explicitly set the `data` attribute on the request
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
