from rest_framework import serializers

from product.exceptions import (
    InvalidTitleException,
    CategoryDoesNotExistException,
    InvalidPriceException,
    InvalidBannerException,
)
from product.models.category import Category
from product.serializers.banner_data_serializer import BannerDataSerializer


class ItemDataSerializer(serializers.Serializer):
    """
    Serializer to validate item creation data, including banners and category.
    """

    title = serializers.CharField(max_length=255)
    category = serializers.IntegerField()
    price = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True, required=False)
    banners = BannerDataSerializer(many=True, required=False)

    def validate_title(self, value):
        """
        Validate the title field.
        """
        if len(value.strip()) == 0:
            raise InvalidTitleException()
        return value

    def validate_category(self, value):
        """
        Validate the category_id field.
        """
        try:
            category = Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise CategoryDoesNotExistException()
        return category

    def validate_price(self, value):
        """
        Validate the price field.
        """
        if value <= 0:
            raise InvalidPriceException()
        return value

    def validate_banners(self, value):
        """
        Validate the banners field.
        """
        for banner in value:
            banner_serializer = BannerDataSerializer(data=banner)
            if not banner_serializer.is_valid():
                raise InvalidBannerException()
        return value
