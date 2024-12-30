from django.urls import path
from product.views.category_view import CategoryListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
]