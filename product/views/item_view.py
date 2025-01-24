from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from product.exceptions import ItemNotFoundException
from product.models.item import Item
from product.serializers.item_creation_serializer import ItemCreationSerializer
from product.serializers.item_serializer import ItemWithImagesSerializer
from product.services.item_creator import create_item_with_banners
from product.throttling import ItemThrottle
from reusable.jwt import CookieJWTAuthentication


class ItemPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"
    max_page_size = 100


class ItemListAllView(generics.ListAPIView):
    """
    View to list all items with search, filters, and ordering.
    Additionally, provides the maximum price of the filtered items.
    """

    serializer_class = ItemWithImagesSerializer
    pagination_class = ItemPagination
    permission_classes = [AllowAny]
    throttle_classes = [ItemThrottle]

    queryset = Item.objects.all()

    # Add filters, search, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ["title"]

    filterset_fields = {
        "category": ["exact"],
        "price": ["gte", "lte"],
    }

    ordering_fields = ["created_at", "price"]
    ordering = ["-created_at"]  # Default ordering (newest first)

    def get(self, request, *args, **kwargs):
        # Fetch the filtered queryset
        filtered_queryset = self.filter_queryset(self.get_queryset())

        # Calculate the maximum price
        max_price = filtered_queryset.aggregate(max_price=Max("price"))[
            "max_price"
        ]

        # Serialize the data
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            return self.get_paginated_response(
                {"items": data, "max_price": max_price}
            )
        else:
            serializer = self.get_serializer(filtered_queryset, many=True)
            return Response({"items": serializer.data, "max_price": max_price})

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
    throttle_classes = [ItemThrottle]

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

    permission_classes = [AllowAny]
    throttle_classes = [ItemThrottle]

    @property
    def serializer_class(self):
        return ItemWithImagesSerializer

    def get(self, request, item_id):
        try:
            item = Item.objects.prefetch_related("banner_set").get(id=item_id)
        except Item.DoesNotExist:
            raise ItemNotFoundException()

        serializer = self.serializer_class(item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemSellerContactView(APIView):
    """
    View to retrieve contact information of the seller of a specific item.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    throttle_classes = [ItemThrottle]

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise ItemNotFoundException()

        seller = item.seller_user

        seller_contact_info = {
            "email": seller.email,
            "phone": seller.phone
        }

        return Response(seller_contact_info, status=status.HTTP_200_OK)
