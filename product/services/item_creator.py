from product.models.item import Item
from product.models.banner import Banner
from product.models.image import Image
from product.models.category import Category
from user.models.user import User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


def create_item_with_banners(data):
    """
    Service to create an item along with its banners.

    Args:
        data (dict): Validated data containing item details and banner information.

    Returns:
        Item: The created item.

    Raises:
        ObjectDoesNotExist: If `seller_user`, `category_id`, or `image_id` do not exist.
        ValueError: If any unexpected issue arises in banner creation.
    """
    with transaction.atomic():

        category = Category.objects.get(id=data["category_id"])
        seller_user = User.objects.get(id=data["seller_user_id"])

        item_data = create_item_data(data, category, seller_user)
        item = Item.objects.create(**item_data)

        create_banners(data, item)

        return item


def create_banners(data, item):
    banners_data = data.get("banners", [])
    for banner_data in banners_data:
        image = Image.objects.get(id=banner_data["image_id"])
        Banner.objects.create(
            item_id=item,
            order=banner_data["order"],
            image=image,
        )


def create_item_data(data, category, seller_user):
    item_data = {
        "title": data["title"],
        "seller_user": seller_user,
        "category_id": category,
        "price": data["price"],
        "description": data.get("description", ""),
    }
    return item_data