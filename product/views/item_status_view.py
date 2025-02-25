from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.exceptions import ItemNotFoundException
from product.models.item import Item
from product.models.purchase_request import PurchaseRequest
from product.validators.validators import (
    validate_sell_item_request,
    validate_reactivate_item_request,
)
from user.services.permission import IsNotBannedUser


class MarkItemAsSoldAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNotBannedUser]

    MARK_ITEM_AS_SOLD_SUCCESS_MSG = {"detail": "آیتم با موفقیت فروخته شد."}

    def post(self, request, item_id):
        """
        Marks an item as sold if it's in reserved status.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise ItemNotFoundException()

        validate_sell_item_request(user, item)

        self.set_item_state_to_sold(item)

        return Response(
            self.MARK_ITEM_AS_SOLD_SUCCESS_MSG, status=status.HTTP_200_OK
        )

    @staticmethod
    def set_item_state_to_sold(item):
        item.state = Item.State.SOLD
        item.save()


class ReactivateItemAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNotBannedUser]

    REACTIVATE_ITEM_SUCCESS_MSG = {"detail": "آیتم فعال شد."}

    def post(self, request, item_id):
        """
        Reactivates an item from reserved status to active status.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise ItemNotFoundException()

        validate_reactivate_item_request(user, item)

        self.reactivate_item(item)

        return Response(
            self.REACTIVATE_ITEM_SUCCESS_MSG, status=status.HTTP_200_OK
        )

    @staticmethod
    def reactivate_item(item):
        with transaction.atomic():
            item.state = Item.State.ACTIVE
            item.save()
            purchase_requests = PurchaseRequest.objects.filter(
                item=item, state=PurchaseRequest.State.ACCEPTED
            )
            purchase_requests.update(state=PurchaseRequest.State.PENDING)
