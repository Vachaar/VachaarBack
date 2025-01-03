from rest_framework import status
from rest_framework.response import Response

from product.models.item import Item
from product.services.banned_item_checker import check_item_banned


def validate_sell_item_request(user, item):
    banned_error = check_item_banned(item)
    if banned_error:
        return banned_error

    if item.seller_user != user:
        return Response({"error": "You are not authorized to change the status of this item."},
                        status=status.HTTP_403_FORBIDDEN)

    if item.state != Item.State.RESERVED:
        return Response({"error": "Item must be in reserved status to mark it as sold."},
                        status=status.HTTP_400_BAD_REQUEST)


def validate_reactivate_item_request(user, item):
    banned_error = check_item_banned(item)
    if banned_error:
        return banned_error

    if item.seller_user != user:
        return Response({"error": "You are not authorized to reactivate this item."}, status=status.HTTP_403_FORBIDDEN)

    if item.state != Item.State.RESERVED:
        return Response({"error": "Item must be in reserved status to reactivate it."},
                        status=status.HTTP_400_BAD_REQUEST)