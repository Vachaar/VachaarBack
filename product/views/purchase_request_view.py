from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.exceptions import ItemNotFoundException
from product.models.item import Item
from product.models.purchase_request import PurchaseRequest
from product.serializers.purchase_creation_serializer import CreatePurchaseRequestSerializer
from product.serializers.purchase_request_serializer import PurchaseRequestSerializer
from product.services.banned_item_checker import check_item_banned
from product.services.purchase_request_acceptor import accept_purchase_request
from product.services.purchase_request_service import create_or_update_purchase_request, \
    get_user_purchase_request_for_item
from product.validators.validators import validate_accept_purchase_request
from reusable.jwt import CookieJWTAuthentication


class CreatePurchaseRequestAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to create a new purchase request.
        """

        serializer = CreatePurchaseRequestSerializer(data=request.data)
        if serializer.is_valid():
            purchase_request = create_or_update_purchase_request(
                item_id=serializer.validated_data.get("item_id"),
                buyer=request.user,
                comment=serializer.validated_data.get("comment"))

            return Response(
                {"request_id": purchase_request.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptPurchaseRequestAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    ACCEPT_PURCHASE_SUCCESS_MSG = {"detail": "آیتم فعال شد."}

    def post(self, request, purchase_request_id):
        """
        Accepts a purchase request and reserves the item.
        """
        user = request.user
        validate_accept_purchase_request(user, purchase_request_id)
        accept_purchase_request(purchase_request_id)
        return Response(self.ACCEPT_PURCHASE_SUCCESS_MSG, status=status.HTTP_200_OK)


class GetPurchaseRequestsForItemView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        """
        Handles GET requests to retrieve all purchase requests for a specific item.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id, seller_user=user)
        except Item.DoesNotExist:
            raise ItemNotFoundException()

        check_item_banned(item)

        purchase_requests = PurchaseRequest.objects.filter(item=item)
        serializer = PurchaseRequestSerializer(purchase_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetBuyerUserPurchaseRequestView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        """
        Handles GET requests to retrieve the purchase request for a specific item.
        """
        user = request.user

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise ItemNotFoundException()

        check_item_banned(item)

        purchase_request = get_user_purchase_request_for_item(item=item, user=user)

        if purchase_request:
            serializer = PurchaseRequestSerializer(purchase_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_200_OK)
