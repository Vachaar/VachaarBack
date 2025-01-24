from rest_framework import permissions


class IsNotBannedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_banned:
            return False
        return True
