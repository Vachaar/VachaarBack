from django.db import transaction

from product.exceptions import (
    SellerUserIsRequiredException,
    ImageNotFoundException,
)
from product.models.banner import Banner
from product.models.image import Image
from product.models.item import Item


def delete_item_with_banners(item_id):
    """
    Service to delete an existing item along with its banners.

    Args:
        item_id: The id of the item to delete.

    Returns:
        Item: The deleted item id.

    Note:
        Uses database transaction to ensure atomicity. If any operation fails,
        all changes will be rolled back. This includes removing item
        before removing the banners.
    """
    with transaction.atomic():
        item = Item.objects.get(id=item_id)
        banners = Banner.objects.filter(item=item)
        images = [banner.image for banner in banners]

        banners.delete()
        for image in images:
            image.delete()
        item.delete()


def edit_item_with_banners(item_id, data, seller_user):
    """
    Service to edit an existing item along with its banners.

    Args:
        item_id: The id of the item to edit.
        data (dict): Validated data containing item details and banner information.
        seller_user: The authenticated user editing the item.

    Returns:
        Item: The updated item.

    Raises:
        SellerUserIsRequiredException: If the `seller_user` is not provided.
        ValueError: If any unexpected issue arises in banner removal or creation.

    Note:
        Uses database transaction to ensure atomicity. If any operation fails,
        all changes will be rolled back. This includes removing existing banners
        before adding new ones.
    """
    if not seller_user:
        raise SellerUserIsRequiredException()

    with transaction.atomic():
        item_data = create_item_data(data, seller_user)
        Item.objects.filter(id=item_id).update(**item_data)
        item = Item.objects.get(id=item_id)

        remove_banners(item)
        create_banners(data, item)

        return item


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


def remove_banners(item):
    banners = Banner.objects.filter(item=item)
    if banners.exists():
        banners.delete()


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
