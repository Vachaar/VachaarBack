from product.exceptions import ItemNotFoundException, InactiveItemException
from product.models.item import Item
from product.services.banned_item_checker import check_item_banned


def validate_purchase_request(item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise ItemNotFoundException()

    if item.state != Item.State.ACTIVE:
        raise InactiveItemException()

    check_item_banned(item)
