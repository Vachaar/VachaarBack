from abc import abstractmethod

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from reusable.models import BaseModel


class ReportStatus(models.TextChoices):
    REVIEWING = "REVIEWING", _("در صف بررسی")
    ACCEPTED = "ACCEPTED", _("قبول شده")
    REJECTED = "REJECTED", _("رد شده")


class ReportReason(models.TextChoices):
    SPAM = "SPAM", _("تکراری یا اسپم")
    AMORAL = "AMORAL", _("غیر‌اخلاقی")
    FRAUD = "FRAUD", _("کلاهبرداری")
    ILLEGAL = "ILLEGAL", _("غیرقانونی")
    PRICE_ISSUE = "PRICE_ISSUE", _("قیمت نادرست")
    CONTACT_ISSUE = "CONTACT_ISSUE", _("اطلاعات تماس نادرست")
    CATEGORY_ISSUE = "CATEGORY_ISSUE", _("دسته‌بندی نادرست")
    RESPONSIVENESS_ISSUE = "RESPONSIVENESS_ISSUE", _("ناموجودی یا پاسخگو نبودن")
    OTHER = "OTHER", _("سایر دلایل")


REASON_FIELD_MAP = {
    ReportReason.SPAM: "spam",
    ReportReason.AMORAL: "amoral",
    ReportReason.FRAUD: "fraud",
    ReportReason.ILLEGAL: "illegal",
    ReportReason.CONTACT_ISSUE: "contact_issue",
    ReportReason.PRICE_ISSUE: "price_issue",
    ReportReason.CATEGORY_ISSUE: "category_issue",
    ReportReason.RESPONSIVENESS_ISSUE: "responsiveness_issue",
    ReportReason.OTHER: "other",
}


class BaseReport(BaseModel):
    spam: int = models.PositiveIntegerField(default=0)

    amoral: int = models.PositiveIntegerField(default=0)

    fraud: int = models.PositiveIntegerField(default=0)

    illegal: int = models.PositiveIntegerField(default=0)

    contact_issue: int = models.PositiveIntegerField(default=0)

    other: int = models.PositiveIntegerField(default=0)

    status: str = models.CharField(
        max_length=128,
        choices=ReportStatus.choices,  # type: ignore
        default=ReportStatus.REVIEWING,
        verbose_name=_("Status"),
    )

    admin_note: str = models.CharField(
        max_length=128,
        choices=ReportReason.choices,  # type: ignore
        default=ReportReason.OTHER,
        verbose_name=_("Admin Note"),
        help_text=_("Notes from admin about this report."),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk} - {self.get_status_display()}"

    @property
    @abstractmethod
    def get_reported_instance(self):
        raise NotImplementedError("Should be implemented in the child class.")

    @abstractmethod
    def notify_ban(self):
        raise NotImplementedError("Should be implemented in the child class.")

    def _validate_reported_instance(self):
        """
        Validate that the reported instance exists and has the required attribute.
        Returns the validated instance.
        """

        reported = self.get_reported_instance

        if not reported:
            raise ValueError(f"Report {self} has no reported instance.")

        if not hasattr(reported, "is_banned"):
            raise ValueError(
                f"The reported {reported} of Report {self} has no attribute 'is_banned'."
            )

        return reported

    def ban(self) -> None:
        """
        Ban the associated reported instance and update report status.
        """
        with transaction.atomic():
            reported = self._validate_reported_instance()

            reported.is_banned = True
            reported.save()

            self.status = ReportStatus.ACCEPTED
            self.save()

            transaction.on_commit(lambda: self.notify_ban())

    def unban(self) -> None:
        """
        Unban the associated reported instance and update report status.
        """

        with transaction.atomic():
            reported = self._validate_reported_instance()

            if reported.is_banned:
                reported.is_banned = False
                reported.save()

                self.status = ReportStatus.REJECTED
                self.save()

            else:
                raise ValueError(f"The reported {reported} is not banned.")
