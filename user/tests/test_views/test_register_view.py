from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from user.exceptions import EmailIsNotValidException
from user.models.user import User
from user.tests.factories.user_factory import UserFactory
from user.views.register_view import RegisterView


class UserRegistrationTests(TestCase):
    def test_create_user_success(self):
        # Arrange
        factory = APIRequestFactory()
        url = reverse(
            "register"
        )  # Adjust the URL name as per your route configuration
        data = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "phone": "09123456789",
        }

        # Act
        request = factory.post(url, data)
        response = RegisterView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["detail"],
            RegisterView.SUCCESS_MESSAGE.get("detail"),
        )
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_create_user_missing_email(self):
        # Arrange
        factory = APIRequestFactory()
        url = reverse("register")
        data = {"password": "securepassword123", "name": "Test User"}

        # Act
        request = factory.post(url, data)
        response = RegisterView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_user_email_already_exists(self):
        # Arrange
        factory = APIRequestFactory()
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
        request = factory.post(url, data)
        response = RegisterView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_throttling(self):
        # Arrange
        factory = APIRequestFactory()
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
            request = factory.post(url, data)
            response = RegisterView.as_view()(request)
        request = factory.post(url, data)
        response = RegisterView.as_view()(request)

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_429_TOO_MANY_REQUESTS
        )  # Too many requests

    def test_create_user_invalid_email_format(self):
        # Arrange
        factory = APIRequestFactory()
        url = reverse("register")
        data = {
            "email": "invalidemail",
            "password": "securepassword123",
            "name": "Test User",
        }

        # Act
        request = factory.post(url, data)
        response = RegisterView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"]["detail"],
            EmailIsNotValidException.default_detail,
        )
