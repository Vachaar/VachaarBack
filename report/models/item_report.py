from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models.item import Item
from report.models.base_report import BaseReport
from report.services import notifier_service


class ItemReport(BaseReport):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name="aggregated_report",
        verbose_name=_("Item"),
        db_index=True,
    )

    price_issue = models.PositiveIntegerField(default=0)

    category_issue = models.PositiveIntegerField(default=0)

    responsiveness_issue = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Item Aggregated Report")
        verbose_name_plural = _("Item Aggregated Reports")

    def __str__(self):
        return f"[Item={self.item.id}] Status={self.get_status_display()}"

    @property
    def get_reported_instance(self):
        return self.item

    def notify_ban(self):
        notifier_service.send_ban_item_email(
            user=self.item.seller_user,
            reason=self.admin_note,
        )
