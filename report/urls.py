from django.urls import path

from report.views.report_view import UserReportView, ItemReportView

urlpatterns = [
    path(
        "user",
        UserReportView.as_view(),
        name="user-report",
    ),
    path(
        "item",
        ItemReportView.as_view(),
        name="item-report",
    ),
]
