from rest_framework import serializers

from product.models.purchase_request import PurchaseRequest


class PurchaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequest
        fields = ['id', 'buyer_user', 'comment', 'state']
