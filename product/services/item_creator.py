from django.db import transaction

from product.exceptions import (
    SellerUserIsRequiredException,
    ImageNotFoundException,
)
from product.models.banner import Banner
from product.models.image import Image
from product.models.item import Item


def create_item_with_banners(data, seller_user):
    """
    Service to create an item along with its banners.

    Args:
        data (dict): Validated data containing item details and banner information.
        seller_user: The authenticated user creating the item.

    Returns:
        Item: The created item.

    Raises:
        ObjectDoesNotExist: If `seller_user`, `category`, or `image_id` do not exist.
        ValueError: If any unexpected issue arises in banner creation.

    Note:
        Uses database transaction to ensure atomicity. If any operation fails,
        all changes will be rolled back.
    """
    if not seller_user:
        raise SellerUserIsRequiredException()

    with transaction.atomic():
        item_data = create_item_data(data, seller_user)
        item = Item.objects.create(**item_data)

        create_banners(data, item)

        return item


def create_banners(data, item):
    banners_data = data.get("banners", [])
    for banner_data in banners_data:
        try:
            image = Image.objects.get(id=banner_data["image_id"])
        except Image.DoesNotExist:
            raise ImageNotFoundException()

        Banner.objects.create(
            item=item,
            order=banner_data["order"],
            image=image,
        )


def create_item_data(data, seller_user):
    item_data = {
        "title": data.get("title"),
        "seller_user": seller_user,
        "category": data.get("category"),
        "price": data.get("price"),
        "description": data.get("description", ""),
    }
    return item_data
