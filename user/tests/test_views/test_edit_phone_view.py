from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory

from user.tests.factories.user_factory import UserFactory
from user.views.edit_phone_view import EditPhoneNumberView


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
