from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models.item import Item
from product.serializers.item_creation_serializer import ItemCreationSerializer
from product.serializers.item_serializer import ItemWithImagesSerializer
from product.services.item_creator import create_item_with_banners
from reusable.jwt import CookieJWTAuthentication


class ItemListView(APIView):
    """
    View to list items for the logged-in user.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        items = Item.objects.filter(seller_user=user)

        serializer = ItemWithImagesSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemListAllView(APIView):
    """
    View to list all items with pagination.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10

        paginated_items = paginator.paginate_queryset(items, request)
        serializer = ItemWithImagesSerializer(paginated_items, many=True)

        return paginator.get_paginated_response(serializer.data)


class ItemCreateView(APIView):
    """
    View to create an item along with its banners.
    Request:
        - title: str
        - seller_user: int
        - category_id: int
        - price: decimal
        - description: str (optional)
        - banners: list[int]

    Response:
        201:
            - item_id: int
        400:
            - detail: str
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemCreationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                created_item = create_item_with_banners(
                    serializer.validated_data, request.user
                )
                return Response(
                    {"item_id": created_item.id}, status=status.HTTP_201_CREATED
                )
            except (ValueError, ValidationError) as e:
                return Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailView(APIView):
    """
    View to retrieve a single item by ID.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response(
                {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ItemWithImagesSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
