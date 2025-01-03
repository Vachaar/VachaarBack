from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models.item import Item
from product.serializers.item_serializer import ItemWithImagesSerializer


class ProfileItemsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles GET requests to filter items by specific conditions for the logged-in user.
        """
        user = request.user
        filter_group = request.query_params.get('filter_group')

        if not filter_group:
            return Response({"error": "filter_group parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        if filter_group == 'reserved_by_user':
            items = Item.objects.filter(buyer_user=user, state=Item.State.RESERVED)
        elif filter_group == 'bought_by_user':
            items = Item.objects.filter(buyer_user=user, state=Item.State.SOLD)
        elif filter_group == 'sold_by_user':
            items = Item.objects.filter(seller_user=user, state=Item.State.SOLD)
        elif filter_group == 'created_by_user_active':
            items = Item.objects.filter(seller_user=user, state=Item.State.ACTIVE)
        elif filter_group == 'created_by_user_reserved':
            items = Item.objects.filter(seller_user=user, state=Item.State.RESERVED)
        else:
            return Response({"error": "Invalid filter_group parameter."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ItemWithImagesSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
