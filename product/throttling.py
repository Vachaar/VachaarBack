from reusable.throttling import BaseCustomThrottle


class CategoryThrottle(BaseCustomThrottle):
    scope = "category"


class ImageThrottle(BaseCustomThrottle):
    scope = "image"


class ItemThrottle(BaseCustomThrottle):
    scope = "item"
