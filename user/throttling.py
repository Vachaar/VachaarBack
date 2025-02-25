from reusable.throttling import BaseCustomThrottle


class LoginThrottle(BaseCustomThrottle):
    scope = "login"


class RegisterThrottle(BaseCustomThrottle):
    scope = "register"


class VerifyEmailThrottle(BaseCustomThrottle):
    scope = "verify_email"


class ResendVerificationEmailThrottle(BaseCustomThrottle):
    scope = "resend_verification_email"
