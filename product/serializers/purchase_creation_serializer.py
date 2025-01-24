from rest_framework import serializers

from product.models.purchase_request import PurchaseRequest
from product.validators.validators import validate_purchase_request


class CreatePurchaseRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a purchase request.
    """

    item_id = serializers.IntegerField(write_only=True)
    comment = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    request_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = ["item_id", "comment", "request_id"]

    def validate_item_id(self, value):
        validate_purchase_request(value)
        return value
