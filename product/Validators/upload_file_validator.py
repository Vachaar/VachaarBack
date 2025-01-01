from rest_framework.response import Response
from rest_framework import status

def validate_file_size(file, max_size_mb):
    """
    Validates the size of an uploaded file.

    Args:
        file: The uploaded file object.
        max_size_mb (int): The maximum allowed size in megabytes.

    Returns:
        Response or None: A Response object with an error if the file size exceeds the limit, otherwise None.
    """
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    if file.size > max_size:
        return Response(
            {"detail": f"File size exceeds the {max_size_mb}MB limit."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None