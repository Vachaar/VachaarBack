from django.urls import path
from product.views.category_view import CategoryListView
from product.views.image_view import ImageUploadView, ImageRawView
from product.views.item_view import ItemListView, ItemCreateView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:image_id>/', ImageRawView.as_view(), name='image-raw'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/create', ItemCreateView.as_view(), name='create-item')
]