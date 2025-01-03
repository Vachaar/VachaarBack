from rest_framework import status
from rest_framework.response import Response


def check_item_banned(item):
    if item.is_banned:
        return Response({"error": "This item is banned."}, status=status.HTTP_403_FORBIDDEN)
