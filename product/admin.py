from django.contrib import admin

from reusable.admin import BaseAdmin
from .models.banner import Banner
from .models.category import Category
from .models.item import Item
from .models.violation import Violation


@admin.register(Item)
class ItemAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(BaseAdmin):
    pass


@admin.register(Violation)
class ViolationAdmin(BaseAdmin):
    pass
