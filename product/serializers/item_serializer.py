from rest_framework import serializers

from product.models.banner import Banner
from product.models.item import Item


class ItemWithImagesSerializer(serializers.ModelSerializer):
    image_ids = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "category_id",
            "price",
            "description",
            "image_ids",
        ]

    def get_image_ids(self, obj):
        # Get all banners related to this item and extract their image IDs
        return Banner.objects.filter(item_id=obj).values_list(
            "image_id", flat=True
        )
