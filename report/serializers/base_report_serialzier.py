from rest_framework import serializers

from report.exceptions import ReasonIsNotValid
from report.models.base_report import ReportReason


class BaseReportSerializer(serializers.Serializer):
    reason = serializers.ChoiceField(
        choices=ReportReason.choices,
        write_only=True,
        help_text="Reason for reporting.",
    )

    reported_field = (
        None  # Define the specific field to be overridden in subclasses
    )
    report_class = (
        None  # Define the specific report model class to be overridden
    )

    def validate_reason(self, value):
        """
        Validate the reason field.
        """
        valid_reasons = [choice[0] for choice in ReportReason.choices]

        if value not in valid_reasons:
            raise ReasonIsNotValid()

        return value

    def validate(self, attrs):
        if not self.reported_field or not self.report_class:
            raise ValueError(
                "You must define 'reported_field' and 'report_class' in the subclass."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        reported_instance = validated_data[self.reported_field]
        reason = validated_data["reason"]

        report, created = self.report_class.objects.get_or_create(
            **{self.reported_field: reported_instance},
        )

        # Increment the specific report field
        report.inc(reason=reason)
        return report
