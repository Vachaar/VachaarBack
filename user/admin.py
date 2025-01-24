from django.contrib import admin

from reusable.admin import BaseAdmin
from .models.user import User


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_email_verified",
    )
    search_fields = (
        "email",
        "phone",
    )
