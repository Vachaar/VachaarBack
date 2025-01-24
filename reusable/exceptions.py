from typing import Optional

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(
    exc: Exception, context: dict
) -> Optional[Response]:
    """
    Custom exception handler for DRF that modifies the default error response.

    It adds additional fields like a custom error code, a message, and a localized error message (`message_fa`).

    Args:
        exc (Exception): The exception instance raised.
        context (dict): Context dictionary containing request and view information.

    Returns:
        Optional[Response]: Modified response object or None if exception is not handled by DRF.
    """
    # Let DRF handle the standard exception response first
    response = exception_handler(exc, context)

    if response is not None:
        # Extract the default code and detail from the exception (if available)
        error_code: str = getattr(exc, "default_code", "unknown")
        message: str = getattr(exc, "default_detail", "")

        # Build the custom error response
        error_response = {
            "error": response.data,  # Original error data from DRF
            "code": error_code,  # Error code (e.g., "invalid" or "unknown")
            "message": message,  # Default error message in English
            "message_fa": getattr(
                exc, "default_detail_fa", "مشکلی پیش آمده است"
            ),  # Localized error message (Persian)
        }

        # Overwrite the response data with the custom format
        response.data = error_response

    return response


class CustomException(Exception):
    """
    Base class for project-specific custom exceptions.

    Attributes:
        default_message (str): The default error message used for this exception.
    """

    default_message: str = "An error occurred"

    def __init__(self, message: Optional[str] = None) -> None:
        """
        Initializes the exception with a custom message or the default message.

        Args:
            message (str, optional): The custom error message. Defaults to `default_message`.
        """
        super().__init__(message or self.default_message)


class CustomApiValidationError(APIException):
    """
    Custom API Exception for validation errors.

    Attributes:
        status_code (int): The corresponding HTTP status code for the exception.
        default_detail (str): The default error message.
        default_code (str): The default error code.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "Invalid input"
    default_code: str = "invalid"


class EmailCanNotBeSentException(CustomApiValidationError):
    default_detail: str = "مشکل در ارسال ایمیل. لطفا دقایقی بعد تلاش کنید"
    default_code: str = "email can not be sent."
