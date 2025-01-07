from product.exceptions import UnauthorizedPurchaseActionRequest, PurchaseRequestNotFoundException
from product.models.purchase_request import PurchaseRequest
from product.services.banned_item_checker import check_item_banned


def validate_accept_purchase_request(user, purchase_request_id):
    """
    Validates the accept purchase request API requirements.
    """

    try:
        purchase_request = PurchaseRequest.objects.get(id=purchase_request_id)
    except PurchaseRequest.DoesNotExist:
        raise PurchaseRequestNotFoundException()

    item = purchase_request.item

    check_item_banned(item)

    if item.seller_user != user:
        raise UnauthorizedPurchaseActionRequest()
