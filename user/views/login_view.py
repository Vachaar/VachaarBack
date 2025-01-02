from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.exceptions import InvalidCredentialsException
from user.serializers.user_serializer import CustomTokenObtainPairSerializer
from user.throttling import LoginThrottle


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginThrottle]

    LOGIN_SUCCESS_MSG = {"detail": "User logged in successfully."}

    def post(self, request, *args, **kwargs):
        user = self._authenticate_user(request)
        if not user:
            self.get_throttles()[0].throttle_failure(request)
            raise InvalidCredentialsException()

        tokens = super().post(request, *args, **kwargs).data

        response = Response(
            data=self.LOGIN_SUCCESS_MSG,
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="access",
            value=tokens.get("access"),
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        response.set_cookie(
            key="refresh",
            value=tokens.get("refresh"),
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return response

    @classmethod
    def _authenticate_user(cls, request):
        return authenticate(
            request=request,
            username=request.data.get("email"),
            password=request.data.get("password"),
        )
