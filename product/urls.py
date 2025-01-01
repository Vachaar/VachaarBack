from django.urls import path

from product.views.category_view import CategoryListView
from product.views.image_view import ImageUploadView, ImageRawView
from product.views.item_view import ItemListView, ItemCreateView, ItemListAllView, ItemDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:image_id>/', ImageRawView.as_view(), name='image-raw'),
    path('items/', ItemListAllView.as_view(), name='item-list-all'),
    path('items/profile', ItemListView.as_view(), name='profile-item-list'),
    path('items/<int:item_id>/', ItemDetailView.as_view(), name='item-detail'),
    path('items/create', ItemCreateView.as_view(), name='create-item')
]
