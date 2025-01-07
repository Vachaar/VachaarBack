from product.exceptions import UnauthorizedPurchaseActionRequest, ItemWasNotReservedRequest
from product.models.item import Item
from product.services.banned_item_checker import check_item_banned


def validate_sell_item_request(user, item):
    check_item_banned(item)

    if item.seller_user != user:
        raise UnauthorizedPurchaseActionRequest()

    if item.state != Item.State.RESERVED:
        raise ItemWasNotReservedRequest()


def validate_reactivate_item_request(user, item):
    check_item_banned(item)

    if item.seller_user != user:
        raise UnauthorizedPurchaseActionRequest()

    if item.state != Item.State.RESERVED:
        raise ItemWasNotReservedRequest()
