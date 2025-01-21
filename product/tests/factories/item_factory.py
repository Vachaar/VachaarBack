import factory

from product.models.item import Item


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item
