from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from product.tests.factories.category_factory import CategoryFactory
from product.views.item_view import (
    ItemCreateView,
    ItemListAllView, )
from report.models.item_report import ItemReport
from report.models.user_report import UserReport
from report.views.report_view import ItemReportView, UserReportView
from user.models.user import User
from user.tests.factories.user_factory import UserFactory


class ReportTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.seller_user = UserFactory()
        self.buyer_user = UserFactory()
        self.category = CategoryFactory()
        self.another_category = CategoryFactory()

        self.create_item_view = ItemCreateView.as_view()
        self.create_url = reverse("create-item")

        self.create_payload = {
            "title": "Test Item 1",
            "category": self.category.id,
            "price": 50.00,
            "description": "Test Description",
            "banners": [],
        }
        self.create_item_request = self.factory.post(
            self.create_url, data=self.create_payload, format="json"
        )

    def test_create_item_then_report_and_ban(self):
        # item creation
        force_authenticate(self.create_item_request, user=self.seller_user)
        create_item_response = self.create_item_view(self.create_item_request)
        self.assertEqual(create_item_response.status_code, status.HTTP_201_CREATED)
        item_id = create_item_response.data["item_id"]

        # report item
        report_payload = {
            "item": item_id,
            "reason_id": 1
        }
        report_url = reverse("create-item")
        report_item_request = self.factory.post(
            report_url, data=report_payload, format="json"
        )
        force_authenticate(report_item_request, user=self.buyer_user)
        report_item_response = ItemReportView.as_view()(report_item_request)
        self.assertEqual(report_item_response.status_code, status.HTTP_200_OK)

        # get all items before ban
        list_url = reverse("item-list-all")
        list_items_view = ItemListAllView.as_view()
        search_request = self.factory.get(list_url)
        force_authenticate(search_request, user=self.buyer_user)
        search_response = list_items_view(search_request)
        self.assertEqual(len(search_response.data["results"]["items"]), 1)

        # ban item
        ItemReport.objects.first().ban()

        # get all items after ban
        search_request = self.factory.get(list_url)
        force_authenticate(search_request, user=self.buyer_user)
        search_response = list_items_view(search_request)
        self.assertEqual(len(search_response.data["results"]["items"]), 0)

    def test_report_and_ban_user(self):
        # report user
        report_payload = {
            "user": self.seller_user.sso_user_id,
            "reason_id": 1
        }

        report_url = reverse("user-report")
        report_user_request = self.factory.post(
            report_url, data=report_payload, format="json"
        )
        force_authenticate(report_user_request, user=self.buyer_user)
        report_user_response = UserReportView.as_view()(report_user_request)
        self.assertEqual(report_user_response.status_code, status.HTTP_200_OK)

        # create item
        force_authenticate(self.create_item_request, user=self.seller_user)
        create_item_response = self.create_item_view(self.create_item_request)
        self.assertEqual(create_item_response.status_code, status.HTTP_201_CREATED)

        # ban user
        UserReport.objects.first().ban()
        self.assertEqual(User.objects.filter(sso_user_id= self.seller_user.sso_user_id).first().is_banned, True)

        # get all items after ban user
        list_url = reverse("item-list-all")
        list_items_view = ItemListAllView.as_view()
        search_request = self.factory.get(list_url)
        force_authenticate(search_request, user=self.buyer_user)
        search_response = list_items_view(search_request)
        self.assertEqual(len(search_response.data["results"]["items"]), 0)
