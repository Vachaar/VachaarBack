from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reusable.jwt import CookieJWTAuthentication
from user.serializers.user_serializer import (
    EditPhoneSerializer,
    ProfileSerializer,
)


class ProfileView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


class EditPhoneNumberView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    SUCCESS_MESSAGE = {"detail": "شماره با موفقیت تغییر کرد"}

    def post(self, request):
        serializer = EditPhoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response(self.SUCCESS_MESSAGE, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
