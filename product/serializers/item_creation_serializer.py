from rest_framework import serializers

from product.models.category import Category
from product.serializers.banner_data_serializer import BannerDataSerializer


class ItemCreationSerializer(serializers.Serializer):
    """
    Serializer to validate item creation data, including banners and category.
    """

    title = serializers.CharField(max_length=255)
    category = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_blank=True, required=False)
    banners = BannerDataSerializer(many=True, required=False)

    def validate_title(self, value):
        """
        Validate the title field.
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError(
                "Title cannot be blank or whitespace."
            )
        return value

    def validate_category(self, value):
        """
        Validate the category_id field.
        """
        category = Category.objects.filter(id=value).first()
        if not category:
            raise serializers.ValidationError(
                f"Category with ID {value} does not exist."
            )
        return category

    def validate_price(self, value):
        """
        Validate the price field.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value

    def validate_description(self, value):
        """
        Validate the description field.
        """
        max_word_count = 100
        if len(value.split()) > max_word_count:
            raise serializers.ValidationError(
                f"Description must not exceed {max_word_count} words."
            )
        return value

    def validate_banners(self, value):
        """
        Validate the banners field.
        """
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError(
                "At least one banner must be provided."
            )
        for banner in value:
            banner_serializer = BannerDataSerializer(data=banner)
            if not banner_serializer.is_valid():
                raise serializers.ValidationError(
                    f"Invalid banner data: {banner_serializer.errors}"
                )
        return value
