from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.exceptions import (
    UserNotFoundException,
    EmailAlreadyVerifiedException,
    EmailIsNotValidException,
    VerificationCodeIsRequiredException,
    VerificationCodeIsNotValidException,
)
from user.models.user import User
from user.serializers.user_serializer import UserRegistrationSerializer
from user.services.register_email_service import send_verification_email
from user.throttling import (
    RegisterThrottle,
    ResendVerificationEmailThrottle,
    VerifyEmailThrottle,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    throttle_classes = [RegisterThrottle]

    SUCCESS_MESSAGE = {"detail": "ثبت نام موفق. کد تائید به ایمیل شما ارسال شد"}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data.get("email"):
                raise EmailIsNotValidException()

            user = serializer.save()
            return self._handle_successful_registration(user, serializer)

        return self._handle_throttle_failure(serializer, request)

    def _handle_successful_registration(self, user, serializer):
        send_verification_email(user)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(
            data=self.SUCCESS_MESSAGE,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def _handle_throttle_failure(self, serializer, request):
        throttle_class = self.get_throttles()[0]
        throttle_class.throttle_failure(request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    throttle_classes = [ResendVerificationEmailThrottle]

    EMAIL_RESENT_SUCCESS_MSG = {"detail": "کد تائید بازارسال شد"}

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = User.get_user_by_email(email)

        if not user:
            raise UserNotFoundException()

        if user.is_email_verified:
            raise EmailAlreadyVerifiedException()

        send_verification_email(user)
        return Response(
            self.EMAIL_RESENT_SUCCESS_MSG, status=status.HTTP_200_OK
        )


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    throttle_classes = [VerifyEmailThrottle]

    VERIFY_EMAIL_SUCCESS_MSG = {"detail": "ایمیل با موفقیت تائید شد"}

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        verification_code = request.data.get("code")

        if not email:
            raise EmailIsNotValidException()

        if not verification_code:
            raise VerificationCodeIsRequiredException()

        user = User.get_user_by_email(email)
        if not user:
            raise UserNotFoundException()

        if not self._verify_email(user, verification_code):
            raise VerificationCodeIsNotValidException()

        return self._success_response(user)

    @classmethod
    def _verify_email(cls, user, code):
        return (
            user.verification_code == code
            and user.verification_code_expires_at > timezone.now()
        )

    @classmethod
    def _success_response(cls, user):
        user.is_email_verified = True
        user.verification_code = None
        user.verification_code_expires_at = None
        user.save()

        refresh = RefreshToken.for_user(user)

        response = Response(
            data=cls.VERIFY_EMAIL_SUCCESS_MSG,
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        response.set_cookie(
            key="access",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="Strict",
        )

        return response
