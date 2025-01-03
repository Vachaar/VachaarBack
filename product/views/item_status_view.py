from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models.item import Item
from product.validators.item_change_state_validator import validate_sell_item_request, validate_reactivate_item_request


class MarkItemAsSoldAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        """
        Marks an item as sold if it's in reserved status.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        validate_sell_item_request(user, item)

        self.set_item_state_to_sold(item)

        return Response({"message": f"Item sold to {item.buyer_user.username}."}, status=status.HTTP_200_OK)


    @staticmethod
    def set_item_state_to_sold(item):
        item.state = Item.State.SOLD
        item.save()


class ReactivateItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        """
        Reactivates an item from reserved status to active status.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        validation_error = validate_reactivate_item_request(user, item)
        if validation_error:
            return validation_error

        self.reactivate_item(item)

        return Response({"message": "Item reactivated."}, status=status.HTTP_200_OK)

    @staticmethod
    def reactivate_item(item):
        item.state = Item.State.ACTIVE
        item.save()
