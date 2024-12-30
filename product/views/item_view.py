from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models.item import Item
from rest_framework.permissions import IsAuthenticated

from product.serializers.item_creation_serializer import ItemCreationSerializer
from product.serializers.item_serializer import ItemWithImagesSerializer
from product.services.item_creator import create_item_with_banners


class ItemListView(APIView):
    """
    View to list items for the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        items = Item.objects.filter(seller_user=user)

        serializer = ItemWithImagesSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ItemCreateView(APIView):
    """
    View to create an item along with its banners.
    """

    def post(self, request):
        serializer = ItemCreationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                created_item = create_item_with_banners(serializer.validated_data)
                return Response({"item_id": created_item.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
