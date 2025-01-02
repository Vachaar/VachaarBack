from reusable.exceptions import CustomApiValidationError


class UserNotFoundException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "کاربر مورد نظر یافت نشد"
    default_code: str = "user not found."


class EmailIsNotValidException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "ایمیل معتبر نیست"
    default_code: str = "invalid email."


class EmailAlreadyVerifiedException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "این ایمیل قبلا تائید شده است"
    default_code: str = "email is already verified."


class VerificationCodeIsRequiredException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "کد تائید الزامی است"
    default_code: str = "verification code is required."


class VerificationCodeIsNotValidException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "کد تائید نامعتبر است"
    default_code: str = "verification code is not valid."


class InvalidCredentialsException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "احراز نامعتبر"
    default_code: str = "invalid credentials."
