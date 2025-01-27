from rest_framework import serializers

from report.exceptions import ReasonIsNotValid
from report.models.base_report import ReportReason

REASON_MAPPING = {
    1: ReportReason.FRAUD,
    2: ReportReason.ILLEGAL,
    3: ReportReason.AMORAL,
    4: ReportReason.PRICE_ISSUE,
    5: ReportReason.CONTACT_ISSUE,
    6: ReportReason.CATEGORY_ISSUE,
    7: ReportReason.RESPONSIVENESS_ISSUE,
    8: ReportReason.SPAM,
    9: ReportReason.OTHER,
}


class BaseReportSerializer(serializers.Serializer):
    reported_field = (
        None  # Define the specific field to be overridden in subclasses
    )
    report_class = (
        None  # Define the specific report model class to be overridden
    )

    reason_id = serializers.IntegerField(
        write_only=True,
    )

    def validate_reason_id(self, value):
        """
        Validate the reason field using the frontend mapping.
        """

        if value not in REASON_MAPPING:
            raise ReasonIsNotValid()

        return REASON_MAPPING[value]

    def validate(self, attrs):
        if not self.reported_field or not self.report_class:
            raise ValueError(
                "You must define 'reported_field' and 'report_class' in the subclass."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        reported_instance = validated_data[self.reported_field]
        reason = validated_data["reason_id"]

        report, created = self.report_class.objects.get_or_create(
            **{self.reported_field: reported_instance},
        )

        # Increment the specific report field
        report.inc(reason=reason)
        return report
