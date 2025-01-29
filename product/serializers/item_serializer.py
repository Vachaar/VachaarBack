from rest_framework import serializers

from product.models.banner import Banner
from product.models.item import Item
from product.models.purchase_request import PurchaseRequest


class ItemWithImagesSerializer(serializers.ModelSerializer):
    image_ids = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField(read_only=True)
    has_purchase_request = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "category",
            "price",
            "description",
            "is_banned",
            "image_ids",
            "is_owner",
            "has_purchase_request",
        ]

    def get_image_ids(self, obj):
        # Get all banners related to this item and extract their image IDs
        return (
            Banner.objects.filter(item_id=obj)
            .order_by("order")
            .values_list("image_id", flat=True)
        )

    def get_is_owner(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        return obj.seller_user == user

    def get_has_purchase_request(self, obj):
        return (
            True if PurchaseRequest.objects.filter(item=obj).exists() else False
        )
