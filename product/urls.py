from django.urls import path

from product.views.category_view import CategoryListView
from product.views.image_view import ImageUploadView, ImageRawView
from product.views.item_status_view import (
    MarkItemAsSoldAPIView,
    ReactivateItemAPIView,
)
from product.views.item_view import (
    ItemCreateView,
    ItemListAllView,
    ItemDetailView,
    ItemSellerContactView,
)
from product.views.profile_items_view import ProfileItemsAPIView
from product.views.purchase_request_view import (
    GetBuyerUserPurchaseRequestView,
    GetPurchaseRequestsForItemView,
    AcceptPurchaseRequestAPIView,
    CreatePurchaseRequestAPIView,
)

urlpatterns = [
    path("categories", CategoryListView.as_view(), name="category-list"),
    path("images/upload", ImageUploadView.as_view(), name="image-upload"),
    path("images/<int:image_id>", ImageRawView.as_view(), name="image-raw"),
    path('items/contact-info/<int:item_id>/', ItemSellerContactView.as_view(), name='item-contact-info'),
    path("items/create", ItemCreateView.as_view(), name="create-item"),
    path("items/<int:item_id>", ItemDetailView.as_view(), name="item-detail"),
    path("items", ItemListAllView.as_view(), name="item-list-all"),
    path("items/profile/<str:filter_group>", ProfileItemsAPIView.as_view(), name="profile-item-list"),
    path("items/<int:item_id>/reactivate", ReactivateItemAPIView.as_view(), name="reactivate_item"),
    path("items/<int:item_id>/sold", MarkItemAsSoldAPIView.as_view(), name="mark_item_as_sold"),

    path("purchase-requests/create", CreatePurchaseRequestAPIView.as_view(), name="create-purchase-request"),

    path("purchase-requests/accept/<int:purchase_request_id>", AcceptPurchaseRequestAPIView.as_view(),
         name="accept-purchase-request"),
    path("purchase-requests/item/<int:item_id>", GetPurchaseRequestsForItemView.as_view(),
         name="get-purchase-requests-for-item"),
    path("purchase-requests/buyer/<int:item_id>", GetBuyerUserPurchaseRequestView.as_view(),
         name="get-buyer-user-purchase-request"),
]
