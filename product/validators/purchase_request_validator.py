from rest_framework import status
from rest_framework.response import Response

from product.models.item import Item
from product.services.banned_item_checker import check_item_banned


def validate_purchase_request(item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({"error": f"Item with id {item_id} does not exist."},
                        status=status.HTTP_400_BAD_REQUEST)

    if item.state != Item.State.ACTIVE:
        return Response({"error": "Item is not available for purchase."},
                        status=status.HTTP_400_BAD_REQUEST)

    item_banned_error = check_item_banned(item)
    if item_banned_error:
        return item_banned_error


