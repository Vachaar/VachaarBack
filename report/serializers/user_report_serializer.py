from rest_framework import serializers

from report.exceptions import UserDoesNotExist
from report.models.user_report import UserReport
from report.serializers.base_report_serialzier import BaseReportSerializer
from user.models.user import User


class UserReportSerializer(BaseReportSerializer):
    user = serializers.IntegerField(
        write_only=True,
        help_text="ID of the user being reported.",
    )

    reported_field = "user"
    report_class = UserReport

    def validate_user(self, value):
        try:
            return User.objects.get(pk=value)
        except User.DoesNotExist:
            raise UserDoesNotExist()
