from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from user.admin import UserAdmin
from user.models.user import User


class AdminUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            phone="09123456789",
            is_active=True,
            is_staff=False,
        )

        self.user_admin = UserAdmin(model=User, admin_site=AdminSite())

    def test_user_admin_list_display(self):
        # Assert
        self.assertEqual(
            self.user_admin.list_display,
            (
                "email",
                "first_name",
                "last_name",
                "phone",
                "is_active",
                "is_staff",
            ),
        )

    def test_user_admin_list_filter(self):
        # Assert
        self.assertEqual(
            self.user_admin.list_filter,
            (
                "is_staff",
                "is_active",
                "is_email_verified",
            ),
        )

    def test_user_admin_search_fields(self):
        # Assert
        self.assertEqual(
            self.user_admin.search_fields,
            (
                "email",
                "phone",
            ),
        )
