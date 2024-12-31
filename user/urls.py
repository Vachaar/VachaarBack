from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import register_view, login_view, stat_view

urlpatterns = [
    path(
        "register/",
        register_view.RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        login_view.CustomTokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="refresh_token",
    ),
    path(
        "verify-email/",
        register_view.VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path(
        "resend-verification-email/",
        register_view.ResendVerificationEmailCodeView.as_view(),
        name="resend-verification-email",
    ),
    path(
        "user_stats/",
        stat_view.render_admin_stats_view,
        name="user-stats",
    ),
]
