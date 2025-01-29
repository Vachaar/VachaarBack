from django.contrib import admin

from reusable.admin import BaseAdmin
from .models.banner import Banner
from .models.category import Category
from .models.image import Image
from .models.item import Item
from .models.purchase_request import PurchaseRequest


@admin.register(Item)
class ItemAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(BaseAdmin):
    pass


@admin.register(Image)
class ImageAdmin(BaseAdmin):
    pass


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(BaseAdmin):
    pass
