from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer
from product.throttling import CategoryThrottle


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    throttle_classes = [CategoryThrottle]
