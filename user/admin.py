from django.contrib import admin

from reusable.admin import BaseAdmin
from .models.offender import OffenderUser
from .models.user import User


@admin.register(User)
class UserAdmin(BaseAdmin):
    pass


@admin.register(OffenderUser)
class OffenderUserAdmin(BaseAdmin):
    pass
