import factory
from factory.django import DjangoModelFactory

from product.models.purchase_request import PurchaseRequest
from product.tests.factories.item_factory import ItemFactory
from user.tests.factories.user_factory import UserFactory


class PurchaseRequestFactory(DjangoModelFactory):
    class Meta:
        model = PurchaseRequest

    item = factory.SubFactory(ItemFactory)
    buyer_user = factory.SubFactory(UserFactory)
    comment = factory.Faker('sentence')
    state = PurchaseRequest.State.PENDING
