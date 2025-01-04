from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models.item import Item
from product.serializers.item_creation_serializer import ItemCreationSerializer
from product.serializers.item_serializer import ItemWithImagesSerializer
from product.services.item_creator import create_item_with_banners
from reusable.jwt import CookieJWTAuthentication


class ItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ItemListAllView(generics.ListAPIView):
    """
    View to list all items with search, filters, and ordering.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemWithImagesSerializer
    pagination_class = ItemPagination

    queryset = Item.objects.all()

    # Add filters, search, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ["title"]

    filterset_fields = {
        "category_id": ["exact"],
        "price": ["gte", "lte"],
    }

    ordering_fields = ["created_at", "price"]
    ordering = ["-created_at"]  # Default ordering (newest first)


class ItemListView(ItemListAllView):
    """
    View to list items for the logged-in user.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(seller_user=self.request.user)


class ItemCreateView(APIView):
    """
    View to create an item along with its banners.
    Request:
        - title: str
        - category: int
        - price: decimal
        - description: str (optional)
        - banners: list[BannerDataSerializer]

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

    @property
    def serializer_class(self):
        return ItemWithImagesSerializer

    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        serializer = self.serializer_class(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
