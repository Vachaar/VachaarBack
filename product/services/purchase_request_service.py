from product.models.item import Item
from product.models.purchase_request import PurchaseRequest


def create_or_update_purchase_request(item_id, buyer, comment):
    item = Item.objects.get(id=item_id)

    purchase_request, created = PurchaseRequest.objects.update_or_create(
        item=item,
        buyer_user=buyer,
        defaults={"comment": comment}
    )

    return purchase_request


def get_user_purchase_request_for_item(item, user):
    return PurchaseRequest.objects.filter(item=item, buyer_user=user).first()
