from typing import Any, Optional, Tuple

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


class BaseAdmin(admin.ModelAdmin):
    """
    A base admin class that adds default readonly fields for all models.
    """

    base_readonly_fields: Tuple[str, str, str] = (
        "id",
        "created_at",
        "updated_at",
    )

    def get_readonly_fields(
        self, request: HttpRequest, obj: Optional[Any] = None
    ) -> Tuple[str, ...]:
        """
        Combines the base readonly fields with the model-specific readonly fields.
        """
        if self.readonly_fields:
            return tuple(self.readonly_fields) + self.base_readonly_fields
        return self.base_readonly_fields


class BasePermissionMixin:
    """
    A customizable mixin to disable specific admin permissions.
    Override class variables to control allowed actions.
    """

    allow_add: bool = True
    allow_change: bool = True
    allow_delete: bool = True

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Determines if the add action is allowed.
        """
        return self.allow_add

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[Any] = None
    ) -> bool:
        """
        Determines if the change action is allowed.
        """
        return self.allow_change

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[Any] = None
    ) -> bool:
        """
        Determines if the delete action is allowed.
        """
        return self.allow_delete

    def save_model(
        self, request: HttpRequest, obj: Any, form: Any, change: bool
    ) -> None:
        """
        Restricts saving the model unless the add or change action is explicitly allowed.
        """
        if not self.allow_add and not change:
            raise PermissionDenied("Adding new entries is not allowed.")
        if not self.allow_change and change:
            raise PermissionDenied("Updating entries is not allowed.")

    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        """
        Restricts deleting the model if the delete permission is disabled.
        """
        if not self.allow_delete:
            raise PermissionDenied("Deleting entries is not allowed.")

    def save_related(
        self, request: HttpRequest, form: Any, formsets: Any, change: bool
    ) -> None:
        """
        Restricts saving related models if saving is disabled.
        """
        if not self.allow_add and not change:
            raise PermissionDenied("Adding related entries is not allowed.")
        if not self.allow_change and change:
            raise PermissionDenied("Updating related entries is not allowed.")


class ReadOnlyAdminMixin(BasePermissionMixin):
    """
    A mixin to make the admin interface completely read-only.
    """

    allow_add: bool = False
    allow_change: bool = False
    allow_delete: bool = False


class UnRemovableAdminMixin(BasePermissionMixin):
    """
    A mixin to disable the change and delete actions in the admin interface.
    """

    allow_add: bool = True
    allow_change: bool = False
    allow_delete: bool = False


class UnWritableAdminMixin(BasePermissionMixin):
    """
    A mixin to disable the add and change actions in the admin interface.
    """

    allow_add: bool = False
    allow_change: bool = False
    allow_delete: bool = True
