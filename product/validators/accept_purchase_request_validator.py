from rest_framework import status
from rest_framework.response import Response

from product.models.purchase_request import PurchaseRequest
from product.services.banned_item_checker import check_item_banned


def validate_accept_purchase_request(user, purchase_request_id):
    """
    Validates the accept purchase request API requirements.
    """

    try:
        purchase_request = PurchaseRequest.objects.get(id=purchase_request_id)
    except PurchaseRequest.DoesNotExist:
        return Response({"error": "Purchase request not found."}, status=status.HTTP_404_NOT_FOUND)

    item = purchase_request.item

    banned_item_error = check_item_banned(item)
    if banned_item_error:
        return banned_item_error

    if item.seller_user != user:
        return Response({"error": "You are not authorized to accept this purchase request."},
                        status=status.HTTP_403_FORBIDDEN)

    return None