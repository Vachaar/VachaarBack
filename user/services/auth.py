from rest_framework.permissions import BasePermission

from reusable.utils import get_cf_ident


class IsAccepted(BasePermission):
    """
    Allows access only to verified profiles.
    """

    def has_permission(self, request, view):
        pass


class IsClient(BasePermission):
    def has_permission(self, request, view):
        ip = get_cf_ident(request)
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.client
            and request.user.client.check_ip(ip)
        )
