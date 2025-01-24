from django.conf import settings
from django.contrib import admin
from django.db.models import F
from django.utils.html import format_html

from report.models.item_report import ItemReport
from report.models.user_report import UserReport
from reusable.admin import BaseAdmin


class BaseReportAdmin(BaseAdmin):
    """
    Base admin class for handling common report functionalities for reports.
    """

    list_filter = ("status",)
    readonly_fields = (
        "spam",
        "amoral",
        "fraud",
        "illegal",
        "contact_issue",
        "other",
    )

    def get_queryset(self, request):
        """
        Annotate the queryset with the total_reports field for ordering.
        """
        qs = (
            super()
            .get_queryset(request)
            .annotate(
                total_reports=(
                    F("spam")
                    + F("amoral")
                    + F("fraud")
                    + F("illegal")
                    + F("contact_issue")
                    + F("other")
                )
            )
        )
        return qs.order_by("-total_reports")

    def total_reports(self, obj):
        """
        Retrieve the total number of reports for this object from the annotated field.
        """
        return obj.total_reports

    total_reports.short_description = "Total Reports"

    def ban(self, request, queryset):
        for report in queryset:
            report.ban()
        self.message_user(request, "Selected reports have been banned.")

    def unban(self, request, queryset):
        for report in queryset:
            report.unban()
        self.message_user(request, "Selected reports have been unbanned.")

    actions = ["ban", "unban"]


@admin.register(UserReport)
class UserReportAdmin(BaseReportAdmin):
    """
    Admin panel configuration for User Reports.
    """

    list_display = ("user", "status", "total_reports", "admin_note")
    search_fields = ("user__email", "user__phone")
    actions = ["ban_report", "unban_report"]


@admin.register(ItemReport)
class ItemReportAdmin(BaseReportAdmin):
    """
    Admin panel configuration for Item Reports.
    """

    list_display = (
        "link_to_item",
        "item",
        "status",
        "total_reports",
        "admin_note",
    )
    search_fields = ("item__title",)

    # Extend the readonly fields specific to ItemReport
    readonly_fields = BaseReportAdmin.readonly_fields + (
        "price_issue",
        "category_issue",
        "responsiveness_issue",
        "link_to_item",
    )

    def get_queryset(self, request):
        """
        Override queryset to include additional fields specific to ItemReport.
        """
        qs = (
            super()
            .get_queryset(request)
            .annotate(
                total_reports=(
                    F("spam")
                    + F("amoral")
                    + F("fraud")
                    + F("illegal")
                    + F("contact_issue")
                    + F("price_issue")
                    + F("category_issue")
                    + F("responsiveness_issue")
                    + F("other")
                )
            )
        )
        return qs.order_by("-total_reports")

    def link_to_item(self, obj):
        """
        Provides a link to view the item on the website.
        """
        item_url = f"{settings.BASE_URL}/product/items/{obj.item.id}/"
        return format_html(
            '<a href="{}" target="_blank">View Item</a>', item_url
        )

    link_to_item.short_description = "Item Page"

    def ban_user(self, request, queryset):
        """
        Ban the seller of the reported item.
        """
        for report in queryset:
            seller = report.item.seller_user
            if seller:
                seller.is_banned = True
                seller.save()
                seller.sold_items.update(is_banned=True)

        self.message_user(request, "Selected users have been banned.")

    actions = BaseReportAdmin.actions + ["ban_user"]
