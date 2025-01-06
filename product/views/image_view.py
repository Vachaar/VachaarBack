from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.exceptions import NoFileProvidedException, ImageNotFoundException
from product.models.image import Image
from product.services.upload_file_validator import (
    validate_file_size,
    validate_file_type,
)
from reusable.jwt import CookieJWTAuthentication


class ImageUploadView(APIView):
    """
    API to upload images.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if "file" not in request.FILES:
            raise NoFileProvidedException()

        file = request.FILES["file"]

        validate_file_size(
            file=file,
            max_size_mb=settings.IMAGE_MAX_SIZE_MB,
        )

        validate_file_type(
            file=file,
            allowed_types=[
                f"image/{file_type.strip()}"
                for file_type in settings.ALLOWED_IMAGE_TYPES.split(", ")
            ],
        )

        image = Image.objects.create(
            content_type=file.content_type,
            image_data=file.read(),
        )
        return Response({"id": image.id}, status=status.HTTP_201_CREATED)


class ImageRawView(APIView):
    """
    API to serve raw image data for embedding in HTML.
    """

    permission_classes = [AllowAny]

    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise ImageNotFoundException()
        return HttpResponse(image.image_data, content_type=image.content_type)
