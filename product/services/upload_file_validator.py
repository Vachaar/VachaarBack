from typing import Any, List

from product.exceptions import (
    FileSizeExceedMaxSizeException,
    InvalidFileTypeException,
)


def validate_file_size(file: Any, max_size_mb: int) -> Any:
    """
    Validates whether the size of the given file is within the specified maximum size
    limit. If the file size exceeds the maximum size, an exception is raised.

    :param file: The file object to be validated. The object must have a `size`
                 property indicating its size in bytes.
    :param max_size_mb: The maximum allowed size for the file, specified in
                        megabytes.
    :return: The validated file object if its size is within the specified limits.
    :raises FileSizeExceedMaxSizeException: If the file size exceeds the
                                             specified maximum size.
    """
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    if file.size > max_size:
        raise FileSizeExceedMaxSizeException()
    return file


def validate_file_type(file: Any, allowed_types: List[str]) -> Any:
    """
    Validates the MIME type of provided file against a list of allowed types. If the file type
    is not within the allowed types, an error response indicating the permitted types and an
    HTTP 400 status code is returned. If the file type is valid, the file is returned unchanged.

    :param file: The file object to validate.
    :type file: Any
    :param allowed_types: A list of acceptable MIME types for the file.
    :type allowed_types: List[str]
    :return: The file object if its MIME type is valid.
    :rtype: Any
    """
    if file.content_type not in allowed_types:
        raise InvalidFileTypeException()
    return file
