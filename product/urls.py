from django.urls import path
from product.views.category_view import CategoryListView
from product.views.images_view import ImageUploadView, ImageRawView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:image_id>/', ImageRawView.as_view(), name='image-raw')
]