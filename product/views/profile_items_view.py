from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.exceptions import InvalidProfileItemsFilterGroup
from product.models.item import Item
from product.serializers.item_serializer import ItemWithImagesSerializer
from reusable.jwt import CookieJWTAuthentication


class ProfileItemsAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, filter_group):
        """
        Handles GET requests to filter items by specific conditions for the logged-in user.
        """
        user = request.user

        if not filter_group:
            raise InvalidProfileItemsFilterGroup()

        filter_map = {
            "reserved_by_user": Q(buyer_user=user, state=Item.State.RESERVED),
            "bought_by_user": Q(buyer_user=user, state=Item.State.SOLD),
            "sold_by_user": Q(seller_user=user, state=Item.State.SOLD),
            "created_by_user_active": Q(
                seller_user=user, state=Item.State.ACTIVE
            ),
            "created_by_user_reserved": Q(
                seller_user=user, state=Item.State.RESERVED
            ),
            "banned": Q(seller_user=user, is_banned=True),
        }

        query_filter = filter_map.get(filter_group)

        if not query_filter:
            raise InvalidProfileItemsFilterGroup()

        items = Item.objects.filter(query_filter)
        serializer = ItemWithImagesSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
