from rest_framework import serializers

from product.models.purchase_request import PurchaseRequest


class PurchaseRequestSerializer(serializers.ModelSerializer):
    buyer_user_phone = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseRequest
        fields = ["id", "buyer_user_phone", "comment", "state"]

    def get_buyer_user_phone(self, obj):
        return obj.buyer_user.phone if obj.buyer_user else None
