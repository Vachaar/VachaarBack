from django.test import TestCase
from django.urls import reverse
from rest_framework.test import force_authenticate, APIRequestFactory

from user.tests.factories.user_factory import UserFactory
from user.views.profile_view import EditPhoneNumberView, ProfileView


class ProfileTests(TestCase):
    def setUp(self):
        self.user = UserFactory(
            email="test@example.com",
            password="test password",
            phone="09000000000",
        )

    def test_get_profile_successfully(self):
        # Arrange
        view = ProfileView.as_view()
        url = reverse("profile")
        request = APIRequestFactory().get(url, format="json")
        force_authenticate(request, user=self.user)

        # Act
        response = view(request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["phone"], "09000000000")

    def test_get_profile_unauthorized(self):
        # Arrange
        view = ProfileView.as_view()
        url = reverse("profile")
        request = APIRequestFactory().get(url, format="json")

        # Act
        response = view(request)

        # Assert
        self.assertEqual(response.status_code, 401)


class EditPhoneNumberTests(TestCase):
    def setUp(self):
        self.user = UserFactory(
            email="test@example.com",
            password="test password",
            phone="09000000000",
        )

    def test_edit_phone_successfully(self):
        # Arrange
        view = EditPhoneNumberView.as_view()

        data = {"phone": "09011111111"}
        url = reverse("edit-phone")
        request = APIRequestFactory().post(url, data=data, format="json")

        force_authenticate(request, user=self.user)

        # Act
        response = view(request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "09011111111")

    def test_edit_phone_validation_error(self):
        # Arrange
        view = EditPhoneNumberView.as_view()

        data = {"phone": "0901111111"}
        url = reverse("edit-phone")
        request = APIRequestFactory().post(url, data=data, format="json")

        force_authenticate(request, user=self.user)

        # Act
        response = view(request)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "09000000000")


class EditPhoneNumberTests(TestCase):
    def setUp(self):
        self.user = UserFactory(
            email="test@example.com",
            password="test password",
            phone="09000000000",
        )

    def test_edit_phone_successfully(self):
        # Arrange
        view = EditPhoneNumberView.as_view()

        data = {"phone": "09011111111"}
        url = reverse("edit-phone")
        request = APIRequestFactory().post(url, data=data, format="json")

        force_authenticate(request, user=self.user)

        # Act
        response = view(request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "09011111111")

    def test_edit_phone_validation_error(self):
        # Arrange
        view = EditPhoneNumberView.as_view()

        data = {"phone": "0901111111"}
        url = reverse("edit-phone")
        request = APIRequestFactory().post(url, data=data, format="json")

        force_authenticate(request, user=self.user)

        # Act
        response = view(request)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "09000000000")
