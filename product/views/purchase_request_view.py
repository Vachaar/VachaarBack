from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models.item import Item
from product.models.purchase_request import PurchaseRequest
from product.serializers.purchase_request_serializer import PurchaseRequestSerializer
from product.services.banned_item_checker import check_item_banned
from product.services.purchase_request_acceptor import accept_purchase_request
from product.services.purchase_request_service import create_or_update_purchase_request, get_user_purchase_request_for_item
from product.validators.accept_purchase_request_validator import validate_accept_purchase_request
from product.validators.purchase_request_validator import validate_purchase_request

class CreatePurchaseRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to create a new purchase request.
        """
        user = request.user  # Get the logged-in user
        data = request.data
        item_id = data.get("item_id")
        comment = data.get("comment", "")

        validation_result = validate_purchase_request(item_id)
        if validation_result:
            return validation_result

        purchase_request = create_or_update_purchase_request(item_id=item_id, buyer=user, comment=comment)

        return Response(
            {"message": "Purchase request created successfully.", "request_id": purchase_request.id},
            status=status.HTTP_201_CREATED,
        )


class AcceptPurchaseRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, purchase_request_id):
        """
        Accepts a purchase request and reserves the item.
        """
        user = request.user

        validation_error = validate_accept_purchase_request(user, purchase_request_id)
        if validation_error:
            return validation_error

        accept_purchase_request(purchase_request_id)

        return Response({"message": "Purchase request accepted and item reserved."}, status=status.HTTP_200_OK)


class GetPurchaseRequestsForItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        """
        Handles GET requests to retrieve all purchase requests for a specific item.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id, seller_user=user)
        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found or you are not the seller."},
                status=status.HTTP_404_NOT_FOUND
            )

        item_banned_error = check_item_banned(item)
        if item_banned_error:
            return item_banned_error

        purchase_requests = PurchaseRequest.objects.filter(item=item)
        serializer = PurchaseRequestSerializer(purchase_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetBuyerUserPurchaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        """
        Handles GET requests to retrieve the purchase request for a specific item.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        purchase_request = get_user_purchase_request_for_item(item=item, user=user)

        if purchase_request:
            serializer = PurchaseRequestSerializer(purchase_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_200_OK)
