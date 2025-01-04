from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response

from product.services.upload_file_validator import validate_file_size


class ValidateFileSizeTests(TestCase):
    def setUp(self):
        """Set up any necessary test data or default values."""
        self.max_size_mb = 1  # 1 MB limit

    def test_file_size_within_limit(self):
        # Arrange
        file = SimpleUploadedFile(
            "test_file.txt", b"small file content", content_type="text/plain"
        )

        # Act
        result = validate_file_size(file, self.max_size_mb)

        # Assert
        self.assertIsNone(result)

    def test_file_size_exceeds_limit(self):
        # Arrange
        oversized_content = b"x" * (2 * 1024 * 1024)  # 2 MB file
        file = SimpleUploadedFile(
            "large_file.txt", oversized_content, content_type="text/plain"
        )

        # Act
        result = validate_file_size(file, self.max_size_mb)

        # Assert
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result.data, {"detail": "File size exceeds the 1MB limit."}
        )

    def test_file_with_zero_size(self):
        # Arrange
        file = SimpleUploadedFile(
            "empty_file.txt", b"", content_type="text/plain"
        )

        # Act
        result = validate_file_size(file, self.max_size_mb)

        # Assert
        self.assertIsNone(result)

    def test_file_size_exactly_at_limit(self):
        # Arrange
        exact_limit_content = b"x" * (1 * 1024 * 1024)  # 1 MB file
        file = SimpleUploadedFile(
            "exact_limit_file.txt",
            exact_limit_content,
            content_type="text/plain",
        )

        # Act
        result = validate_file_size(file, self.max_size_mb)

        # Assert
        self.assertIsNone(result)
