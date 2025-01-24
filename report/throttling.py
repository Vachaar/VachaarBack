from reusable.throttling import BaseCustomThrottle


class UserReportThrottle(BaseCustomThrottle):
    scope = "user_report"


class ItemReportThrottle(BaseCustomThrottle):
    scope = "item_report"
