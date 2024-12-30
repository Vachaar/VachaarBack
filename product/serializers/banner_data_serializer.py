from rest_framework import serializers
from product.models.image import Image

class BannerDataSerializer(serializers.Serializer):
    """
    Serializer to validate banner data, including image_id and order.
    """

    image_id = serializers.IntegerField()
    order = serializers.IntegerField()

    def validate_image_id(self, value):
        """
        Ensure the provided image_id exists in the Image model.
        """
        if not Image.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Image with ID {value} does not exist.")
        return value

    def validate_order(self, value):
        """
        Validate the order value to ensure it is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Order must be a positive integer.")
        return value
