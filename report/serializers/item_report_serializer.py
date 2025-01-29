from rest_framework import serializers

from product.models.item import Item
from report.exceptions import ItemDoesNotExist
from report.models.item_report import ItemReport
from report.serializers.base_report_serialzier import BaseReportSerializer


class ItemReportSerializer(BaseReportSerializer):
    item = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        write_only=True,
        help_text="ID of the item being reported.",
    )

    reported_field = "item"
    report_class = ItemReport

    def validate_item(self, value):
        if not Item.objects.filter(id=value.id).exists():
            raise ItemDoesNotExist()

        return value
