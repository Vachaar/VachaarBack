from rest_framework import permissions


class IsNotBannedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        return not request.user.is_banned
