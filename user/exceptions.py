from reusable.exceptions import CustomApiValidationError


class UserNotFoundException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "User not found."
    default_code: str = "user not found."


class EmailIsNotValidException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "Invalid email."
    default_code: str = "invalid email."


class EmailAlreadyVerifiedException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "Email is already verified."
    default_code: str = "email is already verified."


class VerificationCodeIsRequiredException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "Verification code is required."
    default_code: str = "verification code is required."


class VerificationCodeIsNotValidException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "Verification code is not valid."
    default_code: str = "verification code is not valid."


class InvalidCredentialsException(CustomApiValidationError):
    status_code: int = 400
    default_detail: str = "Invalid credentials."
    default_code: str = "invalid credentials."
