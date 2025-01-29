from rest_framework import serializers

from product.models.banner import Banner
from product.models.item import Item


class ItemWithImagesSerializer(serializers.ModelSerializer):
    image_ids = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField(read_only=True)

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
