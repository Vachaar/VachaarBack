from typing import Any

from reusable.services import BaseService


class UserValidator:
    """
    A class containing static utility methods for validating user-related information,
    such as phone numbers and national ID values.
    """

    @staticmethod
    def phone_validator(value: Any) -> str:
        """
        Validates if the given value is a valid phone number.

        A valid phone number is a string that starts with '09' followed by 9 digits.

        Args:
            value (Any): The value to be validated.

        Returns:
            str: The validated phone number.

        Raises:
            ValidationError: If the value is not a valid phone number.
        """
        return BaseService.regex_validator(
            value=value,
            pattern=r"09\d{9}",
            error_message="Invalid mobile number",
        )

    @staticmethod
    def national_id_validator(value: Any) -> str:
        """
        Validates if the given value is a valid national ID.

        A valid national ID is a string which has 10 digits.

        Args:
            value (Any): The value to be validated.

        Returns:
            str: The validated national ID.

        Raises:
            ValidationError: If the value is not a valid national ID.
        """
        return BaseService.regex_validator(
            value=value, pattern=r"\d{10}", error_message="Invalid national ID"
        )
