from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from report.serializers.base_report_serialzier import BaseReportSerializer
from report.serializers.item_report_serializer import ItemReportSerializer
from report.serializers.user_report_serializer import UserReportSerializer
from report.throttling import UserReportThrottle, ItemReportThrottle
from reusable.jwt import CookieJWTAuthentication
from user.services.permission import IsNotBannedUser


class BaseReportView(generics.CreateAPIView):
    serializer_class = BaseReportSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsNotBannedUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        report = serializer.save()

        return Response(
            {"id": report.report_class.get_reported_instance.id},
            status=status.HTTP_201_CREATED,
        )


class UserReportView(generics.CreateAPIView):
    serializer_class = UserReportSerializer
    throttle_classes = [
        UserReportThrottle,
    ]


class ItemReportView(generics.CreateAPIView):
    serializer_class = ItemReportSerializer
    throttle_classes = [
        ItemReportThrottle,
    ]
