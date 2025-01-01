from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.Validators.upload_file_validator import validate_file_size, validate_file_type
from product.models.image import Image


class ImageUploadView(APIView):
    """
    API to upload images.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        size_validation_response = validate_file_size(file, max_size_mb=10)
        if size_validation_response is not None:
            return size_validation_response

        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        type_validation_response = validate_file_type(file, allowed_types)
        if type_validation_response:
            return type_validation_response

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
        image = get_object_or_404(Image, id=image_id)
        return HttpResponse(image.image_data, content_type=image.content_type)
