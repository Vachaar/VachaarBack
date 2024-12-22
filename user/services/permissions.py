from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from user.models.user import User


def has_valid_role(user, required_role: str) -> bool:
    """
    Helper function to check if the user has a valid with the required role.

    :param user: The user instance to check.
    :type user: Any
    :param required_role: The role to validate against.
    :type required_role: str
    :return: True if the user has the required role, otherwise False.
    :rtype: bool
    """
    return user and isinstance(user, User) and user.role == required_role


class IsStaff(BasePermission):
    """
    Custom permission class to check if the user has a staff role.

    This permission is primarily used for allowing staff members to access
    certain views or resources in the application.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return has_valid_role(request.user, User.STAFF_USER)


class IsManager(BasePermission):
    """
    Custom permission class to check if the user has a manager role.

    This permission is used to restrict access only for users with managerial rights.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return has_valid_role(request.user, User.MANAGER_USER)


class Can(BasePermission):
    """
    Custom permission class for checking user permissions based on roles and specific permissions.

    This class checks if the user is not a normal user and has a specific required permission.
    """

    perm: str  # Define the permission string that needs to be checked.

    def has_permission(self, request: Request, view: View) -> bool:
        user = request.user
        return (
            user and user.role != User.NORMAL_USER and user.has_perm(self.perm)
        )


class CanUserReport(Can):
    """
    Custom permission class for checking reporting-specific user permissions.

    This class inherits from `Can` and applies the same logic for verifying
    user permissions required for reporting.
    """

    pass
