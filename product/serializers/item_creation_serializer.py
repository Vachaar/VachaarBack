from rest_framework import serializers

from product.models.category import Category
from product.serializers.banner_data_serializer import BannerDataSerializer


class ItemCreationSerializer(serializers.Serializer):
    """
    Serializer to validate item creation data, including banners and category.
    """

    title = serializers.CharField(max_length=255)
    category_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_blank=True, required=False)
    banners = BannerDataSerializer(many=True)

    def validate_category_id(self, value):
        """
        Ensure the provided category_id exists in the Category model.
        """
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f"Category with ID {value} does not exist."
            )
        return value
