from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.exceptions import ImageNotFoundException
from product.models.image import Image
from product.tests.factories.image_factory import ImageFactory
from product.views.image_view import ImageUploadView, ImageRawView
from user.tests.factories.user_factory import UserFactory


class ImageUploadViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ImageUploadView.as_view()
        self.url = reverse("image-upload")
        self.valid_image_file = SimpleUploadedFile(
            name="test_image.jpeg",
            content=b"valid_image_content",
            content_type="image/jpeg",
        )
        self.invalid_file_type = SimpleUploadedFile(
            name="test_image.txt",
            content=b"invalid_file_content",
            content_type="text/plain",
        )
        self.large_image_file = SimpleUploadedFile(
            name="large_image.jpeg",
            content=b"0" * (10 * 1024 * 1024 + 1),
            content_type="image/jpeg",
        )
        self.user = UserFactory()

    def test_upload_without_file(self):
        # Arrange
        request = self.factory.post(self.url, data={})
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_valid_image(self):
        # Arrange
        data = {"file": self.valid_image_file}
        request = self.factory.post(self.url, data, format="multipart")
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertTrue(Image.objects.filter(id=response.data["id"]).exists())

    def test_upload_invalid_file_type(self):
        # Arrange
        data = {"file": self.invalid_file_type}
        request = self.factory.post(self.url, data, format="multipart")
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_large_file(self):
        # Arrange
        data = {"file": self.large_image_file}
        request = self.factory.post(self.url, data, format="multipart")
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Image.objects.exists())

    def test_unauthenticated_access(self):
        # Arrange
        data = {"file": self.valid_image_file}
        request = self.factory.post(self.url, data, format="multipart")

        # Act
        response = self.view(request)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ImageRawViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ImageRawView.as_view()
        self.valid_image_id = 1
        self.invalid_image_id = 999
        self.image = ImageFactory(id=self.valid_image_id)
        self.url = reverse(
            "image-raw", kwargs={"image_id": self.valid_image_id}
        )
        self.invalid_url = reverse(
            "image-raw", kwargs={"image_id": self.invalid_image_id}
        )

    def test_get_image_success(self):
        # Arrange
        request = self.factory.get(self.url)

        # Act
        response = self.view(request, image_id=self.valid_image_id)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content, self.image.image_data)
        self.assertEqual(response["Content-Type"], self.image.content_type)

    def test_get_image_not_found(self):
        # Arrange
        request = self.factory.get(self.invalid_url)

        # Act
        response = self.view(request, image_id=self.invalid_image_id)

        # Assert
        self.assertEqual(response.status_code, 400)
