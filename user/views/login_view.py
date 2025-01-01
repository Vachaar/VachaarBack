from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

from user.exceptions import InvalidCredentialsException
from user.serializers.user_serializer import CustomTokenObtainPairSerializer
from user.throttling import LoginThrottle


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginThrottle]

    def post(self, request, *args, **kwargs):
        user = self._authenticate_user(request)
        if not user:
            self.get_throttles()[0].throttle_failure(request)
            raise InvalidCredentialsException

        token_response = super().post(request, *args, **kwargs)
        return token_response

    @classmethod
    def _authenticate_user(cls, request):
        return authenticate(
            request=request,
            username=request.data.get("email"),
            password=request.data.get("password"),
        )
