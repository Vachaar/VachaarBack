from reusable.exceptions import CustomApiValidationError


class UserNotFoundException(CustomApiValidationError):
    default_detail: str = "کاربر مورد نظر یافت نشد"
    default_code: str = "user not found."


class EmailIsNotValidException(CustomApiValidationError):
    default_detail: str = "ایمیل معتبر نیست"
    default_code: str = "invalid email."


class PhoneIsNotValidException(CustomApiValidationError):
    default_detail: str = "شماره موبایل معتبر نیست"
    default_code: str = "invalid phone."


class UserAlreadyExistsException(CustomApiValidationError):
    default_detail: str = "شما قبلا ثبت نام کرده اید"
    default_code: str = "user already exists."


class EmailAlreadyVerifiedException(CustomApiValidationError):
    default_detail: str = "این ایمیل قبلا تائید شده است"
    default_code: str = "email is already verified."


class VerificationCodeIsRequiredException(CustomApiValidationError):
    default_detail: str = "کد تائید الزامی است"
    default_code: str = "verification code is required."


class VerificationCodeIsNotValidException(CustomApiValidationError):
    default_detail: str = "کد تائید نامعتبر است"
    default_code: str = "verification code is not valid."


class InvalidCredentialsException(CustomApiValidationError):
    default_detail: str = "احراز نامعتبر"
    default_code: str = "invalid credentials."
