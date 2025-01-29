from product.exceptions import ItemNotFoundException, InactiveItemException
from product.exceptions import ItemWasNotReservedRequest
from product.exceptions import (
    UnauthorizedPurchaseActionRequest,
    PurchaseRequestNotFoundException,
)
from product.models.item import Item
from product.models.purchase_request import PurchaseRequest
from product.services.banned_item_checker import check_item_banned


def validate_accept_purchase_request(user, purchase_request_id):
    try:
        purchase_request = PurchaseRequest.objects.get(id=purchase_request_id)
    except PurchaseRequest.DoesNotExist:
        raise PurchaseRequestNotFoundException()

    item = purchase_request.item

    check_item_banned(item)

    if item.seller_user != user:
        raise UnauthorizedPurchaseActionRequest()


def validate_sell_item_request(user, item):
    validate_change_reserved_item_request(user, item)


def validate_reactivate_item_request(user, item):
    validate_change_reserved_item_request(user, item)


def validate_change_reserved_item_request(user, item):
    check_item_banned(item)

    if item.seller_user != user:
        raise UnauthorizedPurchaseActionRequest()

    if item.state != Item.State.RESERVED:
        raise ItemWasNotReservedRequest()


def validate_purchase_request(item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise ItemNotFoundException()

    if item.state != Item.State.ACTIVE:
        raise InactiveItemException()

    check_item_banned(item)
