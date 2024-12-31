from django.core.exceptions import ValidationError
from django.test import TestCase

from user.services.validators import UserValidator


class TestUserValidators(TestCase):
    def test_email_validator_valid_emails(self):
        emails = [
            "test@example.com",
            "user123@domain.org",
            "valid.email+test@sub.domain.co",
        ]
        for email in emails:
            # Act
            validated_email = UserValidator.email_validator(email)

            # Assert
            self.assertEqual(validated_email, email)

    def test_email_validator_invalid_emails(self):
        emails = [
            "invalid-email",
            "missing-at-symbol.com",
            "@missinglocalpart.com",
            "",
        ]
        for email in emails:
            # Act & Assert
            with self.assertRaises(
                ValidationError, msg="Invalid email address"
            ):
                UserValidator.email_validator(email)

    def test_email_validator_none(self):
        # Arrange
        email = None

        # Act & Assert
        with self.assertRaises(ValidationError, msg="Invalid email address"):
            UserValidator.email_validator(email)

    def test_email_validator_whitespace(self):
        # Arrange
        email = "    "

        # Act & Assert
        with self.assertRaises(ValidationError, msg="Invalid email address"):
            UserValidator.email_validator(email)

    def test_phone_validator_valid_numbers(self):
        valid_phone_numbers = ["09123456789", "09234567890", "09345678901"]
        for valid_phone_number in valid_phone_numbers:
            # Act
            result = UserValidator.phone_validator(valid_phone_number)

            # Assert
            self.assertEqual(result, valid_phone_number)

    def test_phone_validator_invalid_numbers(self):
        invalid_phone_numbers = [
            "08123456789",  # Starts with wrong prefix
            "0912345678",  # Too short
            "091234567890",  # Too long
            "abcdefghijk",  # Not numeric
            "+919876543210",  # Contains invalid symbols
        ]
        for invalid_phone_number in invalid_phone_numbers:
            # Act & Assert
            with self.assertRaises(
                ValidationError, msg="Invalid mobile number"
            ):
                UserValidator.phone_validator(invalid_phone_number)

    def test_email_validator_valid(self):
        values = [
            "test@example.com",
            "user123@test.co",
            "name.surname@gmail.com",
        ]
        for value in values:
            # Act
            result = UserValidator.email_validator(value)
            # Assert
            self.assertEqual(result, value)

    def test_email_validator_invalid(self):
        values = ["testexample.com", "user@@test.co", "name@.com", "", None]
        for value in values:
            with self.assertRaises(ValidationError):
                UserValidator.email_validator(value)

    def test_phone_validator_valid(self):
        values = ["09123456789", "09987654321", "09012345678"]
        for value in values:
            # Act
            result = UserValidator.phone_validator(value)
            # Assert
            self.assertEqual(result, value)

    def test_phone_validator_invalid(self):
        values = ["123456789", "0912345678a", "abcd123456", "", None]
        for value in values:
            with self.assertRaises(ValidationError):
                UserValidator.phone_validator(value)

    def test_national_id_validator_valid(self):
        values = ["1234567890", "0987654321", "1111111111"]
        for value in values:
            # Act
            result = UserValidator.national_id_validator(value)
            # Assert
            self.assertEqual(result, value)

    def test_national_id_validator_invalid(self):
        values = ["12345", "12345678901", "abcdefghij", "", None]
        for value in values:
            with self.assertRaises(ValidationError):
                UserValidator.national_id_validator(value)
