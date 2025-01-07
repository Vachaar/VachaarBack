from product.exceptions import BannedItemException


def check_item_banned(item):
    if item.is_banned:
        raise BannedItemException()
