from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.tests.factories.category_factory import CategoryFactory
from product.views.item_status_view import MarkItemAsSoldAPIView
from product.views.item_view import (
    ItemCreateView,
    ItemDetailView,
    ItemListAllView,
    ItemEditView,
    ItemDeleteView,
)
from product.views.profile_items_view import ProfileItemsAPIView
from product.views.purchase_request_view import (
    CreatePurchaseRequestAPIView,
    AcceptPurchaseRequestAPIView,
)
from user.tests.factories.user_factory import UserFactory


class ProductTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.seller_user = UserFactory()
        self.buyer_user = UserFactory()
        self.category = CategoryFactory()
        self.another_category = CategoryFactory()

        self.create_item_view = ItemCreateView.as_view()
        self.create_url = reverse("create-item")

    def test_create_item_and_purchase_request_then_reserve_and_selling_item(
        self,
    ):
        # item creation
        create_payload = {
            "title": "Test Item 1",
            "category": self.category.id,
            "price": 50.00,
            "description": "Test Description",
            "banners": [],
        }
        create_item_request = self.factory.post(
            self.create_url, data=create_payload, format="json"
        )
        force_authenticate(create_item_request, user=self.seller_user)
        create_item_response = self.create_item_view(create_item_request)
        self.assertEqual(
            create_item_response.status_code, status.HTTP_201_CREATED
        )
        item_id = create_item_response.data["item_id"]

        # item detail fetch
        item_detail_request = self.factory.get(
            reverse("item-detail", kwargs={"item_id": item_id})
        )
        force_authenticate(item_detail_request, user=self.buyer_user)
        item_detail_response = ItemDetailView.as_view()(
            item_detail_request, item_id=item_id
        )
        self.assertEqual(item_detail_response.data["id"], item_id)
        self.assertEqual(item_detail_response.data["title"], "Test Item 1")

        # create purchase request
        create_purchase_url = reverse("create-purchase-request")
        data = {"item_id": item_id, "comment": "I want to buy this item."}

        create_purchase_request = self.factory.post(
            create_purchase_url, data, format="json"
        )
        force_authenticate(create_purchase_request, user=self.buyer_user)
        create_purchase_response = CreatePurchaseRequestAPIView.as_view()(
            create_purchase_request
        )
        self.assertEqual(
            create_purchase_response.status_code, status.HTTP_201_CREATED
        )
        purchase_request_id = create_purchase_response.data["request_id"]

        # accept purchase request
        accept_purchase_url = reverse(
            "accept-purchase-request",
            kwargs={"purchase_request_id": purchase_request_id},
        )
        accept_purchase_request = self.factory.post(
            accept_purchase_url, {}, format="json"
        )
        force_authenticate(accept_purchase_request, user=self.seller_user)
        accept_purchase_response = AcceptPurchaseRequestAPIView.as_view()(
            accept_purchase_request, purchase_request_id=purchase_request_id
        )
        self.assertEqual(
            accept_purchase_response.status_code, status.HTTP_200_OK
        )

        # fetch reserved items for buyer
        fetch_reserved_items_url_for_buyer = reverse(
            "profile-item-list", kwargs={"filter_group": "reserved_by_user"}
        )
        fetch_reserved_items_request = self.factory.get(
            fetch_reserved_items_url_for_buyer
        )
        force_authenticate(fetch_reserved_items_request, user=self.buyer_user)
        fetch_reserved_items_response = ProfileItemsAPIView.as_view()(
            fetch_reserved_items_request, filter_group="reserved_by_user"
        )
        self.assert_item_in_response(fetch_reserved_items_response, item_id)

        # fetch reserved items for seller
        fetch_reserved_items_url_for_seller = reverse(
            "profile-item-list",
            kwargs={"filter_group": "created_by_user_reserved"},
        )
        fetch_reserved_items_request = self.factory.get(
            fetch_reserved_items_url_for_seller
        )
        force_authenticate(fetch_reserved_items_request, user=self.seller_user)
        fetch_reserved_items_response = ProfileItemsAPIView.as_view()(
            fetch_reserved_items_request,
            filter_group="created_by_user_reserved",
        )
        self.assert_item_in_response(fetch_reserved_items_response, item_id)

        # sell item
        sell_url = reverse("mark_item_as_sold", kwargs={"item_id": item_id})
        sell_request = self.factory.post(sell_url)
        force_authenticate(sell_request, user=self.seller_user)
        sell_response = MarkItemAsSoldAPIView.as_view()(
            sell_request, item_id=item_id
        )
        self.assertEqual(sell_response.status_code, status.HTTP_200_OK)

        # fetch sold items for buyer
        fetch_sold_items_url_for_buyer = reverse(
            "profile-item-list", kwargs={"filter_group": "bought_by_user"}
        )
        fetch_sold_items_request = self.factory.get(
            fetch_sold_items_url_for_buyer
        )
        force_authenticate(fetch_sold_items_request, user=self.buyer_user)
        fetch_sold_items_response = ProfileItemsAPIView.as_view()(
            fetch_sold_items_request, filter_group="bought_by_user"
        )
        self.assert_item_in_response(fetch_sold_items_response, item_id)

        # fetch reserved items for seller
        fetch_sold_items_url_for_buyer = reverse(
            "profile-item-list", kwargs={"filter_group": "sold_by_user"}
        )
        fetch_sold_items_request = self.factory.get(
            fetch_sold_items_url_for_buyer
        )
        force_authenticate(fetch_sold_items_request, user=self.seller_user)
        fetch_sold_items_response = ProfileItemsAPIView.as_view()(
            fetch_sold_items_request, filter_group="sold_by_user"
        )
        self.assert_item_in_response(fetch_sold_items_response, item_id)

    def test_create_and_searching_item(self):
        # items creation
        creation_payloads = [
            {
                "title": "Test Item1 1",
                "category": self.category.id,
                "price": 50,
                "description": "Test Description1",
                "banners": [],
            },
            {
                "title": "Test Item2 2",
                "category": self.category.id,
                "price": 100,
                "description": "Test Description2",
                "banners": [],
            },
            {
                "title": "Test Item1 3",
                "category": self.another_category.id,
                "price": 10,
                "description": "Test Description3",
                "banners": [],
            },
            {
                "title": "Test Item2 4",
                "category": self.another_category.id,
                "price": 110,
                "description": "Test Description4",
                "banners": [],
            },
        ]

        self.create_and_assert_items(creation_payloads)

        # search
        list_url = reverse("item-list-all")
        search_view = ItemListAllView.as_view()

        # get all items
        search_request = self.factory.get(list_url)
        force_authenticate(search_request, user=self.buyer_user)
        search_response = search_view(search_request)
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data["results"]["items"]), 4)

        # search items by price and title
        search_view = ItemListAllView.as_view()
        list_url = reverse("item-list-all")
        search_request = self.factory.get(
            f"{list_url}?search=Item&price__gte=100&price__lte=110&ordering=price"
        )
        force_authenticate(search_request, user=self.buyer_user)
        search_response = search_view(search_request)

        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data["results"]["items"]), 2)

        result_items = search_response.data["results"]["items"]
        self.assertEqual(result_items[0]["title"], "Test Item2 2")
        self.assertEqual(result_items[1]["title"], "Test Item2 4")

        # search items by category and title
        search_view = ItemListAllView.as_view()
        list_url = reverse("item-list-all")
        search_request = self.factory.get(
            f"{list_url}?search=Item1&category={self.category.id}&ordering=price"
        )
        force_authenticate(search_request, user=self.buyer_user)
        search_response = search_view(search_request)

        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data["results"]["items"]), 1)

        result_items = search_response.data["results"]["items"]
        self.assertEqual(result_items[0]["title"], "Test Item1 1")

    def test_unauthorized_actions_for_buyer_user(self):
        # item creation
        create_payload = {
            "title": "Test Item 1",
            "category": self.category.id,
            "price": 50.00,
            "description": "Test Description",
            "banners": [],
        }
        create_item_request = self.factory.post(
            self.create_url, data=create_payload, format="json"
        )
        force_authenticate(create_item_request, user=self.seller_user)
        create_item_response = self.create_item_view(create_item_request)
        self.assertEqual(
            create_item_response.status_code, status.HTTP_201_CREATED
        )
        item_id = create_item_response.data["item_id"]

        # create purchase request
        create_purchase_url = reverse("create-purchase-request")
        data = {"item_id": item_id, "comment": "I want to buy this item."}
        create_purchase_request = self.factory.post(
            create_purchase_url, data, format="json"
        )
        force_authenticate(create_purchase_request, user=self.buyer_user)
        create_purchase_response = CreatePurchaseRequestAPIView.as_view()(
            create_purchase_request
        )
        self.assertEqual(
            create_purchase_response.status_code, status.HTTP_201_CREATED
        )
        purchase_request_id = create_purchase_response.data["request_id"]

        # accept purchase request unauthorized
        accept_purchase_url = reverse(
            "accept-purchase-request",
            kwargs={"purchase_request_id": purchase_request_id},
        )
        accept_purchase_request = self.factory.post(
            accept_purchase_url, {}, format="json"
        )
        force_authenticate(accept_purchase_request, user=self.buyer_user)
        accept_purchase_response = AcceptPurchaseRequestAPIView.as_view()(
            accept_purchase_request, purchase_request_id=purchase_request_id
        )
        self.assertEqual(
            accept_purchase_response.status_code, status.HTTP_400_BAD_REQUEST
        )

        # edit item unauthorized
        edit_payload = {
            "title": "Test Item 2",
            "category": self.category.id,
            "price": 50.00,
            "description": "Test Description",
            "banners": [],
        }
        edit_url = reverse("edit-item", kwargs={"item_id": item_id})
        edit_item_request = self.factory.put(
            edit_url, data=edit_payload, format="json"
        )
        force_authenticate(edit_item_request, user=self.buyer_user)
        edit_response = ItemEditView.as_view()(edit_item_request, item_id)
        self.assertEqual(edit_response.status_code, status.HTTP_400_BAD_REQUEST)

        # delete item unauthorized
        delete_url = reverse("delete-item", kwargs={"item_id": item_id})
        delete_item_request = self.factory.delete(delete_url, format="json")
        force_authenticate(delete_item_request, user=self.buyer_user)
        delete_response = ItemDeleteView.as_view()(delete_item_request, item_id)
        self.assertEqual(
            delete_response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def create_and_assert_items(self, creation_payloads):
        for creation_payload in creation_payloads:
            create_item_request = self.factory.post(
                self.create_url, data=creation_payload, format="json"
            )
            force_authenticate(create_item_request, user=self.seller_user)
            create_item_response = self.create_item_view(create_item_request)
            self.assertEqual(
                create_item_response.status_code, status.HTTP_201_CREATED
            )

    def assert_item_in_response(self, response, item_id):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], item_id)
