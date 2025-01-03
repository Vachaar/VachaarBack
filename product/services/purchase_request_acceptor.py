from django.db import transaction

from product.models.item import Item
from product.models.purchase_request import PurchaseRequest


def accept_purchase_request(purchase_request_id):
    with transaction.atomic():
        purchase_request = PurchaseRequest.objects.get(id=purchase_request_id)
        purchase_request.state = PurchaseRequest.State.ACCEPTED
        purchase_request.save()

        item = purchase_request.item
        item.state = Item.State.RESERVED
        item.buyer_user = PurchaseRequest.buyer_user
        item.save()
