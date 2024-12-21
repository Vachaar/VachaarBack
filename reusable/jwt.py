from typing import Any

from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import (
    JWTAuthentication as BaseJWTAuthentication,
    AuthUser,
)
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomJWTAuthentication(BaseJWTAuthentication):
    """
    Custom implementation of JWT authentication that extends the base
    functionality of `rest_framework_simplejwt.authentication.JWTAuthentication`.

    Overrides `get_user` to handle cases where the user is not found, raising
    a `PermissionDenied` exception instead of `AuthenticationFailed`.
    """

    def get_user(self, validated_token: Any) -> AuthUser:
        """
        Retrieves the authenticated user based on the validated token.

        If the user is not found (e.g., deleted or inactive), a `PermissionDenied`
        exception is raised. Any other authentication failures are propagated as-is.

        Args:
            validated_token (Any): The JWT token that has been successfully validated.

        Returns:
            AuthUser: The authenticated user instance.

        Raises:
            PermissionDenied: If the user is not found in the system.
            AuthenticationFailed: If any other issue occurs during authentication.
        """
        try:
            # Attempt to get the user using the parent's `get_user` method
            user = super().get_user(validated_token)
            return user
        except AuthenticationFailed as authentication_error:
            # Handle specific cases when the user is not found
            if authentication_error.detail.get("code") == "user_not_found":
                raise PermissionDenied(
                    detail="User not found. Access denied.",
                    code="permission_denied",
                )
            # Re-raise other authentication exceptions as-is
            raise authentication_error
