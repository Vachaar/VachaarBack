from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from report.models.base_report import BaseReport, ReportStatus
from report.models.item_report import ItemReport
from report.services import notifier_service
from user.models.user import User


class UserReport(BaseReport):
    user: User = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="aggregated_report",
        verbose_name=_("User"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("User Aggregated Report")
        verbose_name_plural = _("User Aggregated Reports")

    def __str__(self):
        return (
            f"[Item={self.user.sso_user_id}] Status={self.get_status_display()}"
        )

    @property
    def get_reported_instance(self) -> User:
        return self.user

    def notify_ban(self) -> None:
        notifier_service.send_ban_user_email(
            user=self.user,
            reason=self.admin_note,
        )

    def ban(self) -> None:
        """
        Ban the user and all items where the user is the seller.
        """
        with transaction.atomic():
            # Ban all items of the user
            self.user.sold_items.update(is_banned=True)

            super().ban()

    def unban(self) -> None:
        """
        Unban the user and unban their items that don't have active reports.
        """
        with transaction.atomic():
            # Get the IDs of items that have active (non-REJECTED) reports
            already_reported_item_ids = (
                ItemReport.objects.filter(item__seller_user=self.user)
                .exclude(status=ReportStatus.REJECTED)
                .values_list(
                    "item_id",
                    flat=True,
                )
            )

            # Unban items of the user that are NOT in the reported item list
            self.user.sold_items.exclude(
                id__in=already_reported_item_ids
            ).update(is_banned=False)

            super().unban()
