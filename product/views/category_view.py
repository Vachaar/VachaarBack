from rest_framework.generics import ListAPIView
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer
from rest_framework.permissions import AllowAny

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

